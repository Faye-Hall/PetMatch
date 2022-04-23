import requests, json, functools, operator
from env import API_KEY, API_SECRET_KEY
from models import Favorite, db, Match, Pet, Survey, User
from app import session

CLIENT_ID = API_KEY
CLIENT_SECRET = API_SECRET_KEY


API_BASE_URL = "https://api.petfinder.com/v2/"

def get_headers():
    """Get The Headers For An API Call"""
    CLIENT_ID = API_KEY
    CLIENT_SECRET = API_SECRET_KEY

    data = {
        "grant_type": "client_credentials",
        "client_id": f"{CLIENT_ID}",
        "client_secret": f"{CLIENT_SECRET}",
    }
    response = requests.post(f"{API_BASE_URL}oauth2/token", data = data)
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    
    return headers

def get_pet_info(pet_id):
    """Get The Headers and Parameters for an API Call To Retrieve Pet info From A Survey"""
    headers = get_headers()
    response = requests.get(f"{API_BASE_URL}/animals/{pet_id}", headers = headers)
    
    return response

def get_params(type, age, gender,size,
                               good_with_children,
                               good_with_dogs,
                               good_with_cats,
                               house_trained,
                               location,
                               distance):
    
    if good_with_children  == "true": 
        children_val = "true"
    else:
        children_val = None

    if good_with_dogs == "true": 
        dogs_val = "true"
    else:
        dogs_val = None

    if good_with_cats == "true": 
        cats_val = "true"
    else:
        cats_val = None
    
    if house_trained == "true": 
        house_val = "true"
    else:
        house_val = None

    params = {
        "type":  str(type),
        "age": str(age),
        "gender": str(gender),
        "size": str(size),
        "location": str(location),
        "distance": str(distance),
        "good_with_children": children_val,
        "good_with_dogs": dogs_val,
        "good_with_cats": cats_val,
        "house_trained": house_val,
    }

    
  
    return params
    
def get_survey_matches(params):
    headers = get_headers()
    response = requests.get(f"{API_BASE_URL}/animals/", headers = headers, params = params)
    return response.json()

def add_pets(response):
    
    for pet in response['animals']:
        existing_pet = Pet.query.filter_by(id=pet["id"]).first()

        if existing_pet is None:
            
                if existing_pet is None:
                    pet_id = pet['id'],
                    name = pet['name'],
                    try:
                        image = pet["photos"][0]["medium"]
                    except IndexError:
                        image = 'Not Currently Available',
                    description = pet['description'],
                    location = pet['contact']['address']['postcode'],
                    species = pet['species'],
                    breed = pet['breeds']['primary'],
                    spayed_neutered = pet['attributes']['spayed_neutered'],
                    house_trained = pet['attributes']['house_trained'],
                    special_needs = pet['attributes']['special_needs']
                    new_pet = Pet(
                                id = functools.reduce(operator.add, (pet_id)),
                                name = functools.reduce(operator.add, (name)),
                                image = functools.reduce(operator.add, (image)),
                                description = functools.reduce(operator.add, (description)),
                                location = functools.reduce(operator.add, (location)),
                                species = functools.reduce(operator.add, (species)),
                                breed = functools.reduce(operator.add, (breed)),
                                spayed_neutered = functools.reduce(operator.add, (spayed_neutered)),
                                house_trained = functools.reduce(operator.add, (house_trained)),
                                special_needs = special_needs
                    )
                    new_match = Match(
                                       username = session['username'],
                                       pet_id = functools.reduce(operator.add, (pet_id)),
                                       favorite = ''
                    )
                    db.session.rollback()
                    db.session.add(new_pet)
                    db.session.commit()
                    db.session.add(new_match)
                    db.session.commit()
                    db.session.remove()
        else:
            db.session.commit()

def add_favorite(pet_id):
    """Add A Pet To A User's Favorites List"""
    
    new_favorite = Favorite(

        username = session['username'],
        pet_id = pet_id
        )

    db.session.rollback()
    db.session.add(new_favorite)
    db.session.commit()
    db.session.remove()

def delete_matches():
    """Delete All Matches and Surveys From The Database For A User """
    current_user = session['username']
    matches = Match.query.filter_by(username=current_user).all()
    surveys = Survey.query.filter_by(username=current_user).all()
    for match in matches:
        db.session.delete(match)
        db.session.commit()
    for survey in surveys:
        db.session.delete(survey)
        db.session.commit()
        db.session.remove()
    
def delete_user():
    """Delete A User From The Database"""
    current_user = session['username']
    user = User.query.filter_by(username=current_user).first()  
    db.session.delete(user)
    db.session.commit()
    db.session.remove()          
        
def delete_favorites():
    """Delete All Favorites From The Database For A User"""
    current_user = session['username']
    user = User.query.filter_by(username= current_user).first()
    favorites = Favorite.query.filter_by(username= user.username).all()  
    for favorite in favorites: 
        db.session.delete(favorite)
        db.session.commit()
        db.session.remove()  
        
