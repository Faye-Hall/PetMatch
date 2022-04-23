from wtforms import StringField, PasswordField, EmailField, SelectField, IntegerField, RadioField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length




class RegisterForm(FlaskForm):
    """User Register Form"""

    first_name = StringField("First Name:", validators = [InputRequired()])
        
    last_name = StringField("Last Name:", validators = [InputRequired()])
        
    email = EmailField("Email:", validators = [InputRequired()])
        
    username = StringField("Username:", validators = [InputRequired()])
        
    password = PasswordField("Password:", validators = [InputRequired()])
    
    location = IntegerField("Zipcode", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """User Login Form"""

    username =  StringField("Username:", validators=[InputRequired()])

    password = PasswordField("Password:", validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Edit User Register Form"""

    first_name = StringField("First Name:", validators = [InputRequired()])
        
    last_name = StringField("Last Name:", validators = [InputRequired()])
        
    email = EmailField("Email:", validators = [InputRequired()])

    location = IntegerField("Zipcode", validators=[InputRequired()])
        
class SurveyForm(FlaskForm):
    """User Questionaire Form"""


    type = SelectField(
            "Are you looking for a cat or a dog?",
            choices=[("",""),("cat","Cat"), ("dog","Dog")],
            validators=[InputRequired()]
        )

    age = SelectField(
                    "What age range would you like your pet to be?",
                    choices=[("",""),("baby","Baby"), ("young","Young") ,("adult", "Adult"), ("senior","Senior")],
                    )

    gender = SelectField(
                    "What is your gender preference?",
                    choices=[("",""),("male","Male"), ("female","Female")],
                    validators=[InputRequired()])

    size = SelectField(
            "What size would you like your pet to be?",
            choices=[
                ("",""),
                ("small", "Small"),
                ("medium", "Medium"),
                ("large", "Large"),
                ("small, medium, large, xlarge ", "No Preference")
            ],
            validators=[InputRequired()],
        )

    good_with_children = SelectField(
                    "Are there children in the home?",
                    choices=[("",""),("true","Yes"), ("false","No")],
                    validators=[InputRequired()])

    good_with_dogs = SelectField(
                    "Are there dogs in the home?",
                    choices=[("",""),("true","Yes"), ("false","No")],
                    validators=[InputRequired()])

    good_with_cats = SelectField(
                    "Are there cats in the home?",
                    choices=[("",""),("true","Yes"), ("false","No")],
                    validators=[InputRequired()])

    house_trained = SelectField(
                    "Have you had a pet before?",
                    choices=[("",""),("true","Yes"), ("1","No")],
                    validators=[InputRequired()])

    distance = SelectField(
            "How far are you willing to travel?",
            choices=[("",""),("10", "10 Miles"), ("15", "15 Miles"), ("20", "20 Miles"), ("25","25 Miles"),("50", "50 Miles")],
            validators=[InputRequired()],
        )
