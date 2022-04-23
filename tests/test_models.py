from unittest import TestCase
from app import app
from models import User, Pet, Survey, Match, Favorite, db, connect_db
from flask import Flask, redirect, render_template, session, flash
from test_data import USER_DATA, create_user

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///petfinder_test_db'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dontshow-debug-toolbar']

db.drop_all()
db.create_all()

class ModelTestCase(TestCase):


    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)
        Survey.query.delete()
        Favorite.query.delete()
        Match.query.delete()
        Pet.query.delete()
        User.query.delete()
        
        new_user = User.register(username = 'Test', first_name =  'First', last_name = 'Last', location = 92604, email = 'Email', password = 'Password', survey = [], matches =[], favorites =[])
        
        db.session.add(new_user)
        db.session.commit()

        new_pet = Pet(id=1111,image="https://via.placeholder.com/150?text=no+image+available",name="test",description="testing",location="92604",species="cat",breed="domestic",spayed_neutered="true",special_needs="true",house_trained="true",)
        db.session.add(new_pet)
        db.session.commit()

        new_survey = Survey(id=1111,username='Test',type='cat',age='baby',gender='female',size='small',good_with_children='true',good_with_dogs='true',good_with_cats="true",house_trained='true',distance='10')
        db.session.add(new_survey)
        db.session.commit()

        new_match = Match(id =1111,username='Test',pet_id='1111',favorite='true')
        db.session.add(new_match)
        db.session.commit()
        
        new_favorite = Favorite(id=1111,username='Test',pet_id='1111')
        db.session.add(new_favorite)
        db.session.commit()
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                new_user.authenticate(new_user.username, new_user.password)
            
                self.user = new_user
                self.pet = new_pet
                self.survery = new_survey
                self.match = new_match
                self.favorite = new_favorite
                
                
                session['username'] = self.user.username
                
                
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_User_Model(self):
        
            self.assertEqual(len(User.query.all()), 1)
        
    def test_Pet_Model(self):
        
            self.assertEqual(len(Pet.query.all()), 1)
        
    def test_Survey_Model(self):
        
            self.assertEqual(len(Survey.query.all()), 1)

    def test_Match_Model(self):
        
            self.assertEqual(len(Match.query.all()), 1)
    
    def test_Favorite_Model(self):
        
            self.assertEqual(len(Favorite.query.all()), 1)

            


