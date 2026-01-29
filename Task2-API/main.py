from flask import Flask, flash, redirect, request, render_template, session, url_for
# session 
import json

# import the fetch_and_process function
# as you see we put .first because data.py is in the same folder as main.py
from data import fetch_and_process, get_all_poems
    
app = Flask(__name__)

app.secret_key = "iwillpreparemypapertobethebestinthisworld"


def load_db():
    with open ("Database/users.json","r") as file:
        return json.load(file)
    
    
def save_db(data):
    with open ("Database/users.json", "w") as file:
        json.dump(data, file, indent=4)
 
 
@app.route("/")  
def home():
    # fetch a new poem each time the page is refreshed
    # poems = fetch_and_process() if "poems" not in session else session["poems"]
    
    poems_data  = get_all_poems()
    if "current_index" not in session:
        session["current_index"] = len(poems_data["poems"]) - 1
        
    current_index = session["current_index"]
    # session["poems"] = poems

    return render_template(
        "index.html",
        poem=poems_data["poems"][current_index],
        poemsLength = len(poems_data["poems"]),
        currentIndex=current_index,
        username=session.get("username")
    )
    
@app.route("/next")
def next_poem():
    poems_data = get_all_poems()
    current_index = session.get("current_index", 0)
    
    # if next poem exists, go to next, if not fetch a new one
    if current_index < len(poems_data["poems"]) - 1:
        session["current_index"] = current_index + 1
    else:
        # so here we add a new one in the poem, and then go back to the main list and fetch the last poem
        fetch_and_process()
        print(len(poems_data["poems"]))
        session["current_index"] = len(poems_data["poems"])

    return redirect(url_for("home"))

@app.route("/previous")
def previous_poem():
    current_index = session.get("current_index", 0)
    
    if current_index > 0:
        session["current_index"] = current_index - 1

    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])  
def register_user():
    if request.method == "POST":
        data = load_db()

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        for user in data["users"]:
            if email == user["email"]:
                flash("Email already taken", "error")
                return redirect(url_for("register_user"))


        data["users"].append({
            "id": len(data["users"]),
            "username": username,
            "email": email,
            "password": password
        })

        save_db(data)
        return redirect(url_for("login_user"))

    return render_template("register.html")
    
    # if(request.method == "POST"):
        
    #     data = load_db();
        
    #     username = request.form["username"]
    #     email = request.form["email"]
    #     password = request.form["password"]
        
    #     for user in data["users"]:
    #         if email == user["email"]:
    #             return ("<h1>Email already taken!</h1> <a href='/'>Go Back</a>")
            
    #     data["users"].append({
    #         "id": len(data["users"]) +1,
    #         "username": username,
    #         "email": email,
    #         "password": password
    #     })
        
    #     save_db(data)
        
    #     return render_template("register-success.html", username=username)
    
    # return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        data = load_db()
        email = request.form["email"]
        password = request.form["password"]

        for user in data["users"]:
            if email == user["email"] and password == user["password"]:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["email"] = user["email"]

                flash(f"Welcome back, {user['username']}!", "success")
                return redirect(url_for("home"))

        return "User not found"

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out the current user"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))



app.run(debug=True)