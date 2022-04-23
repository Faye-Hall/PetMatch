"""Models for Petfinder"""

from csv import unregister_dialect
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User Model"""
   
    __tablename__ = "users"

    username = db.Column(db.String,
                         nullable = False,
                         primary_key = True
                         )

    first_name = db.Column(db.String,
                     nullable = False)

    last_name = db.Column(db.String,
                          nullable = False)

    location = db.Column(db.String,
                            nullable = False)
    
    email = db.Column(db.String, 
                      nullable = False)

    password = db.Column(db.String,
                         nullable = False)

    survey = db.relationship('Survey', 
                             backref ='users',
                             
                             )

    matches = db.relationship('Pet',
                                secondary ='matches',
                                backref ='matches_to_user',
                                cascade="all, delete",
                                passive_deletes=True
                                )

    favorites = db.relationship('Pet',
			      secondary ='favorites',
			      backref ='favorites_to_user',
                  cascade="all, delete",
                  passive_deletes=True)
                  


    @classmethod
    def register(cls,username,  first_name, last_name, email, password, survey, matches, favorites, location):
        """Register user w/hased password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')

        user = cls (username = username, first_name = first_name, last_name = last_name, 
        password = hashed_utf8 , email = email, survey = survey, matches = matches, favorites = favorites, location = location)

        #return instance of user with hashed pwd)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """ Validate that user exists & password is correct. Return user if valid; else return False."""

        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):

            return user

        else:
            return False


class Pet(db.Model):
    """Pet Model"""
   
    __tablename__ = "pets"

    id =  db.Column(db.Integer,
                            primary_key = True
                            )

    name = db.Column(db.String,
                     nullable = False,
                     default = 'Not Currently Available')

    image = db.Column(db.String,
                      nullable = False,
                    default = 'Not Currently Available')
    
    description = db.Column(db.String, 
                            nullable = False,
                            default = 'No Description Currently Available')

    
    location = db.Column(db.String,
                        nullable = False)

    species = db.Column(db.String,
                        nullable = False,
                        default = 'No Species Currently Available')

    breed = db.Column(db.String, 
                      nullable = False,
                      default = 'No breed Currently Available')

    spayed_neutered = db.Column(db.String, 
                                nullable = False,
                                default = 'Not Currently Available')

    house_trained = db.Column(db.String, 
                              nullable = False,
                             default = 'Not Currently Available')

    special_needs = db.Column(db.String, 
                              nullable = False,
                              default = 'Not Currently Available')


class Survey(db.Model):
    """Survey Model"""

    __tablename__ = "surveys"

    id = db.Column(db.Integer,
                    primary_key = True,
                     autoincrement = True)
    

    username = db.Column(db.String, 
                        db.ForeignKey('users.username', onupdate="CASCADE"))

    type  =  db.Column(db.String, 
                       nullable = False)

    age  = db.Column(db.String)

    gender  = db.Column(db.String)

    size  =  db.Column(db.String)

    good_with_children = db.Column(db.String)

    good_with_dogs = db.Column(db.String)

    good_with_cats = db.Column(db.String)

    house_trained = db.Column(db.String)
    
    location = db.Column(db.String)

    distance = db.Column(db.Integer)


class Match(db.Model):
    """Match Model"""

    __tablename__ = "matches"

    id = db.Column(db.Integer,
                    primary_key = True,
                     autoincrement = True)

    username = db.Column(db.String, 
                        db.ForeignKey('users.username'), onupdate="CASCADE")

    pet_id = db.Column(db.Integer, 
                       db.ForeignKey('pets.id', onupdate="CASCADE"))

    favorite = db.Column(db.String)

class Favorite(db.Model):
    """Favorites Model"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer,
                    primary_key = True,
                     autoincrement = True)

    username = db.Column(db.String,
                        db.ForeignKey('users.username'), onupdate="CASCADE")

    pet_id = db.Column(db.Integer,
                       db.ForeignKey('pets.id'), onupdate="CASCADE")
