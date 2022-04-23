from unittest import TestCase
from app import app
from models import User, Pet, Survey, Match, Favorite, db, connect_db
from flask import Flask, redirect, render_template, session, flash
from test_data import USER_DATA, create_user

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///petfinder_test_db'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dontshow-debug-toolbar']

#db.create_all()

db.drop_all()
db.create_all()

class RouteTestCase(TestCase):


    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)
        
        
        
        User.query.delete()
        new_user = User.register(username = 'Test', first_name =  'First', last_name = 'Last', location = 92604, email = 'Email', password = 'Password', survey = [], matches =[], favorites =[])
        db.session.add(new_user)
        db.session.commit()
        with app.test_client() as client:
            with client.session_transaction() as session:
                new_user.authenticate(new_user.username, new_user.password)
                
                self.user = new_user
                session['username'] = self.user.username
            
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Homepage</h1>',html)
 
    def test_user_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.user.username
            
            resp = client.get('/Test')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['username'], 'Test')
            self.assertIn('<h2>Your information</h2>',html)
        
    def test_favorites_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.user.username
            resp = client.get('/Test/favorites')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['username'], 'Test')
            self.assertIn('You Have No Favorites',html)
        
    def test_matches_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.user.username
            resp = client.get('/Test/matches')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['username'], 'Test')
            self.assertIn('You Have No Matches',html)
        
    def test_survey_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.user.username
            resp = client.get('/survey')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['username'], 'Test')
            self.assertIn('<h1>Take Our Survey!</h1>',html)


            
         


