# Import relevant modules

from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import url_for
from datetime import timedelta
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days = 2)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

this_directory = os.path.abspath(os.path.dirname(__file__))

path_to_json_file = os.path.join(this_directory, 'persisted_data.json')

if os.path.isfile(path_to_json_file):

    with open(path_to_json_file) as file:
        all_data = json.load(file)

plank_times = all_data["plank_times"]
vo2_maxes = all_data["vo2_maxes"]
total_calories_burned = all_data["total_calories_burned"]
total_distance = all_data["total_distance"]
table_data = all_data["table_data"]
# ivan_monthly_calories = all_data["month_calorie_totals"]["ivan"]
# oliver_monthly_calories = all_data["monthly_calorie_totals"]["oliver"]

# Import the Flask webapp instance that we created in the __init__.py

def put_persisted_data(data_to_be_persisted):
    path_to_data = os.path.join(this_directory, 'persisted_data.json')
    with open(path_to_data, mode="w") as file:
        file.write(json.dumps(data_to_be_persisted, indent=4))
    return 

import secrets 

def get_new_entry(data_of_activity, date_input, competitor, activity_type, score):
    new_entry = dict(data_of_activity=data_of_activity, date_input=date_input, competitor=competitor, activity_type=activity_type, score=score)

    return new_entry

@app.route("/index", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def index():

    # Url arguments can be added to the url like this ?name=Peter&age=57
    # Get the url arguments if there are any
    url_arguments = request.args.to_dict(flat=False)

    # if there are any url arguments, print them to the console here
    if len(url_arguments) > 0:
        print(f"\nThere were some url arguments and they were:\n{url_arguments}\n")

    # When pages contain a form, we can access the variables in this function
    # if the form was submitted
    # Create a default form_package in case the form not submitted
    form_package = {}
    # And now check to see if the form was actually submitted
    if request.method == "POST":

        # pull the form fields into a dictionary for ease
        form_package = request.form.to_dict(flat=False)

        # print the form fields to the console so we can see it was submitted
        print(f"\nThe form was submitted. The data is:\n{form_package}\n")

    return render_template(
        "index.html", form_package=form_package, url_arguments=url_arguments
    )
@app.route("/leaderboard", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def leaderboard():

    competitions = {}
    calories = {}
    planks = {}
    vo2 = {}
    distance = {}
    victory_totals = {}
    victory_totals['Ivan'] = []
    victory_totals['Oliver'] = []

    for player in total_calories_burned:
        player_calories = sum(total_calories_burned[player])
        calories[player] = player_calories
        competitions['calories'] = calories

    for player in vo2_maxes:
        player_vo2_max = max(vo2_maxes[player])
        vo2[player] = player_vo2_max
        competitions['vo2'] = vo2
        
    for player in plank_times:
        player_plank = max(plank_times[player])
        planks[player] = player_plank
        competitions['planks'] = planks
        
    for player in total_distance:
        player_distance = sum(total_distance[player])
        distance[player] = player_distance
        
    for competition in competitions:
        stats = competitions[competition]
        winning_player = max(stats, key=stats.get)
        if winning_player == 'ivan':
            victory_totals['Ivan'].append(competition)
        if winning_player == 'oliver':
            victory_totals['Oliver'].append(competition)

    if len(victory_totals['Oliver']) > len(victory_totals['Ivan']):
        first_place = 'Oliver'
        second_place = 'Ivan'
    
    else:
        first_place = 'Ivan'
        second_place = 'Oliver'

    return render_template(
        "leaderboard.html", 
        first_place = first_place,
        second_place = second_place,
        victory_totals = victory_totals,
    )
@app.route("/running_stats", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def running_stats():

    calories = {}
    planks = {}
    vo2 = {}
    distance = {}

    for player in total_calories_burned:
        player_calories = sum(total_calories_burned[player])
        calories[player] = player_calories

    for player in vo2_maxes:
        player_vo2_max = max(vo2_maxes[player])
        vo2[player] = player_vo2_max

    for player in plank_times:
        player_plank = max(plank_times[player])
        planks[player] = player_plank

    for player in total_distance:
        player_distance = sum(total_distance[player])
        distance[player] = player_distance

    # make a monthly_calories for me and P
    # I need to figure out how to also extract the date from the datetime group
    ivan_monthly_calories = [0,0,0,0,0,0,0,0,0,0,0,0]
    oliver_monthly_calories = [0,0,0,0,0,0,0,0,0,0,0,0]
    for item in table_data:
        for input_type in table_data[item]:
            if input_type == "data_of_activity":
                a = table_data[item][input_type]
                datee = datetime.strptime(a, "%Y-%m-%d")
                month_index = (datee.month) - 1
            if input_type == "competitor":
                competitor = table_data[item][input_type]
            if table_data[item][input_type] == "calories_burned":
                score = table_data[item]["score"]
                if competitor == "oliver":
                    oliver_monthly_calories[month_index] = oliver_monthly_calories[month_index] + score 
                if competitor == "ivan":
                    ivan_monthly_calories[month_index] = ivan_monthly_calories[month_index] + score 

    return render_template(
        "running_stats.html",
        distance = distance,
        planks = planks,
        vo2 = vo2,
        calories = calories,
        ivan_monthly_calories = ivan_monthly_calories,
        oliver_monthly_calories = oliver_monthly_calories
    )
@app.route("/input_form", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def input_form():

    form_package = {}
    # And now check to see if the form was actually submitted
    if request.method == "POST":
        form_package = request.form.to_dict(flat=False)
        print(form_package)
        
        name = form_package["name"][0]
        plank_time = form_package["plank_time"][0]
        vo2_max = form_package["vo2_max"][0]
        calories_burned = form_package["calories_burned"][0]
        distance = form_package["distance"][0]
        data_of_activity = form_package["data_of_activity"][0]
        now = datetime.now() # current date and time
        date_input = now.strftime("%d/%m/%Y, %H:%M:%S")

        if not plank_time == "":
            if plank_time.isdigit():
                plank_time = int(plank_time)
                plank_times[name].append(plank_time)
                table_data_entry = get_new_entry(data_of_activity, date_input, name, "plank", plank_time)
                id=secrets.token_urlsafe(10)
                table_data[id] = table_data_entry
            else:
                flash(
                f"Plank time needs to be a number, you entered {plank_time}.",
                category="warning",
                )
                return redirect(url_for("input_form"))

        if not vo2_max == "":
            if vo2_max.isdigit():
                vo2_max = int(vo2_max)
                vo2_maxes[name].append(vo2_max)
                table_data_entry = get_new_entry(data_of_activity, date_input, name, "vo2_max", vo2_max)
                id=secrets.token_urlsafe(10)
                table_data[id] = table_data_entry                
            else:
                flash(
                f"VO2 Max needs to be a number, you entered {vo2_max}.",
                category="warning",
                )
                return redirect(url_for("input_form"))
            

        if not calories_burned == "":
            if calories_burned.isdigit():
                calories_burned = int(calories_burned)
                total_calories_burned[name].append(calories_burned)
                table_data_entry = get_new_entry(data_of_activity, date_input, name, "calories_burned", calories_burned)
                id=secrets.token_urlsafe(10)
                table_data[id] = table_data_entry
            else:
                flash(
                f"Calories burned needs to be a number, you entered {calories_burned}.",
                category="warning",
                )
                return redirect(url_for("input_form"))
            

        if not distance == "":
            if distance.isalpha():
                flash(
                f"Distance needs to be a number, you entered {distance}.",
                category="warning",
                )
                return redirect(url_for("input_form"))            
            else:
                distance = float(distance)
                total_distance[name].append(distance)
                table_data_entry = get_new_entry(data_of_activity, date_input, name, "distance", distance)
                id=secrets.token_urlsafe(10)
                table_data[id] = table_data_entry         

        put_persisted_data(all_data)
        flash(
            "Your addition has been added to your stats.",
            category="success",
        )
        return redirect(url_for("index"))

    return render_template(
        "input_form.html", form_package=form_package
    )


@app.route("/datatables", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def datatables():

    return render_template(
        "datatables.html",
        plank_times = plank_times,
        vo2_maxes = vo2_maxes,
        total_calories_burned = total_calories_burned,
        total_distance = total_distance,
        table_data = table_data
        )

@app.route("/login", methods=["GET","POST"])

def login():

    if request.method == "POST":
        session.permanent = True
        user = request.form["user"]
        session["user"] = user
        password = request.form["password"]
        
        found_user = users.query.filter_by(username = user).first()

        if found_user:
            session["user"] = found_user.username

        else:
            usr = users(user, password)
            db.session.add(usr)
            db.session.commit()
        flash(
           f"Hello {user}, you have been successfully logged in."   
        )
        return redirect(url_for("user"))

    else:
        if "user" in session:
            user = session["user"]
            flash(
            f"Hello {user}, you are already logged in.", category="success"
            )
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])

def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")

def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    db.create_all()