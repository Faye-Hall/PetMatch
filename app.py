from crypt import methods
from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from env import API_KEY, API_SECRET_KEY, APP_SECRET_KEY
from models import User, Pet, Survey, Match, Favorite, db, connect_db
from forms import RegisterForm, EditUserForm, SurveyForm, LoginForm
from functions import  get_params, get_survey_matches, add_pets, add_favorite, delete_matches, delete_favorites, delete_user
import requests
from werkzeug.exceptions import Unauthorized

API_KEY = ("API_KEY")
API_BASE_URL = "https://api.petfinder.com/v2/"
API_SECRET_KEY = ("API_SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///petfinder_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = APP_SECRET_KEY

connect_db(app)

######################################################## all the pages with forms ########################################################

@app.route('/', methods = ['GET', 'POST'])
def handle_login():
    """Display Login Form And Handle Submission."""
    #session.clear()
    
    form = LoginForm()
    if "username" in session:
        current_user = session['username']
        return redirect(f"/{current_user}")
    else:
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            auth_user = User.authenticate(username, password )

            if auth_user:
                session['username'] = auth_user.username
                return redirect(f"/{session['username']}")

            else: 
                flash(f"Invalid Username/Password")
                return render_template('home_page.html', form = form)

        else:
            return render_template('home_page.html', form = form)
    
@app.route('/<username>')
def display_user(username):
    """Display Current User Info"""

    if "username" in session:
        current_user = User.query.get(username)
        
        if current_user.username == session['username']:
        
            return render_template('user_info.html', current_user = current_user, matches = matches)
        else:
            raise Unauthorized()
    else:
        flash('Login or Register!')
        return redirect('/') 

@app.route('/pet/<int:pet_id>')
def dispay_pet(pet_id):
    """Display Pet Info"""
    if "username" in session:
        current_user = session['username']
        pet = Pet.query.get(pet_id)
        
        return render_template('pet_info.html', current_user = current_user, pet = pet)
    else:
        raise Unauthorized()

@app.route('/register', methods = ['GET','POST'])
def register():
    """Display Register Form And Handle Submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        location = form.location.data
        survey = []
        matches = []
        favorites = []
        
        new_user = User.register(first_name = first_name, last_name = last_name, email = email,
                                    username = username, password = password, survey = survey, matches = matches, 
                                    favorites = favorites,location = location)

        db.session.rollback()
        db.session.add(new_user)
        db.session.commit()
        
        session['username'] = new_user.username
        

        flash(f"Added {first_name} to Database!")

        return redirect(f"/{session['username']}")

    return render_template('register_form.html', form = form)

@app.route('/<username>/edit', methods = ['GET', 'POST'])
def edit_user(username):
    """Display Edit User Form and Handle Submission"""
    
    if "username" in session:
        current_user = User.query.get_or_404(username)
        
        if current_user.username == session['username']:
            form = EditUserForm(obj = current_user)

            if form.validate_on_submit():
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.email = form.email.data
        
                db.session.commit()

                flash(f"{current_user.first_name}'s Changes Updated!")

                return redirect(f"/{session['username']}")
        
        return render_template('user_edit_form.html', current_user = current_user, form = form)
    return Unauthorized()

@app.route('/survey', methods = ['GET', 'POST'])
def survey():
    """Display Survey Form and Handle Submission"""

    form = SurveyForm()

    if "username" in session:
        current_user = session['username']
        this_user = User.query.get(current_user)

        if form.validate_on_submit():
            type = form.type.data
            age = form.age.data
            gender = form.gender.data
            size = form.size.data
            good_with_children = form.good_with_children.data
            good_with_dogs = form.good_with_dogs.data
            good_with_cats = form.good_with_cats.data
            house_trained = form.house_trained.data
            location = this_user.location
            distance = form.distance.data
        
            survey = Survey(username = current_user,
            type = str(type), 
            age = str(age), 
            gender = str(gender), 
            size = str(size),
            good_with_children = str(good_with_children), 
            good_with_dogs = str(good_with_dogs), 
            good_with_cats = str(good_with_cats),
            house_trained = str(house_trained),
            location = str(location), 
            distance = str(distance))

            db.session.rollback()
            db.session.add(survey)
            db.session.commit()
            

            params = get_params(str(type), str(age), str(gender),str(size),
                               (good_with_children),
                               (good_with_dogs),
                               (good_with_cats),
                               (house_trained),
                               str(location),
                               str(distance))
            
            response = (get_survey_matches(params))

            add_pets(response)

            flash(f"Survey Submitted!")

            return redirect(f"/{session['username']}")

        return render_template('survery_form.html', form = form)
    return Unauthorized()


######################################################## all the pages with models ########################################################

@app.route('/<username>/matches')
def matches(username):
    """Display Matched Pets Info"""

    if "username" in session:
        current_user = User.query.get(username)
        
        if current_user.username == session['username']:
            matches = current_user.matches
        
            return render_template('match_list.html', matches = matches, current_user = current_user)
        else:
            raise Unauthorized()
    else:
        flash('Login or Register!')
        return redirect('/')  
    
@app.route('/<pet_id>/add_favorites', methods = ['POST'])
def add_favorites(pet_id):
    """Add Pet to Favorites"""
     
    pet_id = pet_id
    add_favorite(pet_id)

    flash('Added To Favorites!')
    return redirect(f"/{session['username']}/matches")
        
@app.route('/<username>/favorites')
def favorites(username):
    """Display Favorite Pets Info"""
    if "username" in session:
        current_user = User.query.get(username)
        
        if current_user.username == session['username']:
            favorites = current_user.favorites
        
            return render_template('favorite_list.html', favorites = favorites, current_user = current_user)
        else:
            raise Unauthorized()
    else:
        flash('Login or Register!')
        return redirect('/')  

@app.route('/survey/<survey_id>')
def survey_info():
    """Display Survey Info"""

    survey = Survey()
    return render_template('user_info.html', survey = survey)

######################################################## all the pages with deletions ########################################################

@app.route('/logout', methods=['POST'])
def logout_user():
    """Logout Current User"""

    session.clear()
    flash(f"Logout Successful")
    
    return redirect('/')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_current_user(username):
    """Delete Current User Account"""
    
    delete_matches()
    delete_favorites()
    delete_user()
    session.clear()

    flash("Account Deleted!")
    return redirect('/')

@app.route('/delete_matches', methods = ['POST'])
def delete_all_matches():
    """Delete Survey and It's Matches"""
    
    delete_matches()

    flash("All Matches Deleted. Please Start Again")
    return redirect(f"/{session['username']}")

@app.route('/delete_favorites', methods = ['POST'])
def delete_all_favorites():
    """Delete All Favorites"""
    
    delete_favorites()
    return redirect(f"/{session['username']}")

 




















