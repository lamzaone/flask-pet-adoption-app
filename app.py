# Python standard libraries
import json
import os
import sqlite3

# Third party libraries
from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests


# Internal imports
from db import init_db_command
from user import User
from animals import Animal
from adoption_form import AdoptionForm

# Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

print(GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET)
# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.unauthorized_handler
def unauthorized():
    return render_template("unauthorized.html"), 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# redirect to homepage
@app.route("/")
def redirect_to_home():
    return redirect("/home")

# homepage
@app.route("/home")
def index():
    return render_template("index.html")


# Google OAuth2.0
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture,
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



# adoptions page
@app.route("/adoptions")
def adoptions():
    # get the page number from url
    page = int(request.args.get("page", default=1))

    # set the number of items per page
    per_page = 5

    # get animals for the requested page
    animal_posts = Animal.get_all(page, per_page)
    hasForms = False

    if current_user.is_authenticated:
        # first we check if the current user has any forms completed for their posted animals,
        # in order to decide whether to draw the Show Forms button or not.
        if len(AdoptionForm.get_all_by_owner(current_user.id)) > 0:
            hasForms = True

    return render_template("adoptions.html", hasForms=hasForms, animal_posts=animal_posts, page=page, per_page=per_page, Animal=Animal)

@app.route("/adoptions/viewpost", methods=["GET"])
def viewpost():
    # Get animal and post owner info from url
    _id = int(request.args.get("id"))
    animal = Animal.get(_id)
    user = User.get(animal.user_id)
    return render_template("viewpost.html", user=user, _id=_id, animal=animal)


# view completed forms for people who added animals for adoption
@app.route("/forms/view")
@login_required
def viewforms():
    # get all the adoption forms completed for the current user's posts
    adoption_forms = AdoptionForm.get_all_by_owner(current_user.id)

    # if we have forms, then we show them
    if len(adoption_forms) > 0:
        return render_template("viewforms.html", adoption_forms=adoption_forms, User=User, Animal=Animal)
    else:
        return render_template("error_message.html", message="You have nothing to see...")


# see your adoption forms status
@app.route("/forms/status")
@login_required
def myforms():
    # get all the adoption forms completed by current user
    adoption_forms = AdoptionForm.get_all_by_user(current_user.id)

    # if we have forms, then we show them
    if len(adoption_forms) > 0:
        return render_template("myforms.html", adoption_forms=adoption_forms, User=User, Animal=Animal)
    else:
        return render_template("error_message.html", message="Hello! You can fill an adoption formular at any time, and you can check the status here!")

# route to deny an adoption form, by post owner
@app.route("/forms/deny/<string:user_id>/<int:animal_id>", methods=["POST"])
@login_required
def deny_form(user_id, animal_id):
    AdoptionForm.setStatus(user_id, animal_id, "denied")
    return redirect(url_for('viewforms'))

# route to handle form acceptation by post owner
@app.route("/forms/accept/<string:user_id>/<int:animal_id>", methods=["POST"])
@login_required
def accept_form(user_id, animal_id):
    AdoptionForm.setStatus(user_id, animal_id, "accepted")
    Animal.setAdopted(animal_id)
    return redirect(url_for('viewforms'))



# route for adopting an animal, handling both GET and POST requests
@app.route("/adoptions/adopt/<int:animal_id>", methods=["GET", "POST"])
@login_required
def animal_adopt_form(animal_id):
    # Fetch the animal details from the database
    animal = Animal.get(animal_id)

    # Check if the animal exists
    if not animal:
        # Handle the case where the animal does not exist
        return render_template("error_message.html", message="Animal not found")

    if request.method == "POST":
        # Get form data
        user_id = request.form.get("user_id")
        animal_id = request.form.get("animal_id")
        owner_id = request.form.get("owner_id")
        user_age = request.form.get("user_age")
        location = request.form.get("location")
        building_type = request.form.get("building_type")
        current_pets = request.form.get("current_pets")
        previous_experience = request.form.get("previous_experience")
        phone_number = request.form.get("phone_number")

        # Add the new animal to the database
        try:
            AdoptionForm.create(
                user_id = user_id,
                animal_id =animal_id,
                owner_id = owner_id,
                user_age = user_age,
                location = location,
                building_type = building_type,
                current_pets = current_pets,
                previous_experience = previous_experience,
                phone_number = phone_number
            )
        except sqlite3.IntegrityError:
            return render_template("error_message.html", message="You can not complete two forms for the same animal!")

        # redirect back to homepage after creating adoption post
        return redirect(url_for('index'))
    # Pass the animal data to the template
    return render_template("adoption_form.html", animal=animal)

# create a post for animal adoption
@app.route("/adoptions/upload", methods=["GET","POST"])
@login_required
def animal_upload_form():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        location = request.form.get("location")
        print(location)
        kind = request.form.get("kind")
        breed = request.form.get("breed")
        sex = request.form.get("sex")
        age = request.form.get("age")
        description = request.form.get("description")
        img_url = request.form.get("img_url")

        # Add the new animal to the database
        Animal.create(
            name=name,
            user_id=current_user.id,
            kind=kind,
            breed=breed,
            sex=sex,
            age=age,
            description=description,
            img_url=img_url,
            location=location
        )

        # redirect back to homepage after creating adoption post
        return redirect(url_for('index'))

    return render_template("add_adoption_post.html")

# route for completely removing an animal(adoption post) from the database
@app.route("/adoptions/remove/<int:animal_id>", methods=["POST"])
@login_required
def remove_animal(animal_id):
    # make sure the current user owns the animal before removing it,
    # or check if current user is admin
    animal = Animal.get(animal_id)
    if animal and animal.user_id == current_user.id or current_user.is_admin:
        Animal.remove(animal_id)

    return redirect(url_for('index'))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host='127.0.0.1', port='5000')
