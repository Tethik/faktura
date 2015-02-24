from faktura import app
from flask import request, render_template, redirect, abort
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from faktura.models import db, User, TemplateVariable
from passlib.hash import sha256_crypt

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

_trigger_first_time = None
def trigger_first_time():
    global _trigger_first_time
    if _trigger_first_time is None:
        _trigger_first_time = User.query.count() == 0
    return _trigger_first_time

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

def create_user(username, password):
    user = User()
    user.username = username
    user.password = sha256_crypt.encrypt(password)

    db.session.add(user)
    db.session.commit()
    return user


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or sha256_crypt.verify(password, user.password):
        return user
    return None

@app.route("/first_time", methods=["GET", "POST"])
def first_time():
    if not (trigger_first_time() and User.query.count() == 0):
        abort(403)

    vars_to_create = ["companyName","companyStreet","companyCity","companyZip","companyTelephone","companyEmail","companyWebsite","bankgiro"]
    if request.method == "GET" and TemplateVariable.query.count() == 0:
        for var in vars_to_create:
            v = TemplateVariable(var, "")
            db.session.add(v)
        db.session.commit()


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        repeat = request.form["repeat"]

        for var in vars_to_create:
            if request.form.get(var):
                v = TemplateVariable.query.filter_by(key=var).first()
                v.value = request.form.get(var)


        if repeat != password:
            return render_template("first_time.html", msg="Passwords must be the same.")
        user = create_user(username, password)
        user.email = request.form["email"]
        db.session.commit()
        login_user(user)
        return redirect("/")

    return render_template("first_time.html", templateVariables=vars_to_create)

@app.route("/login", methods=["GET", "POST"])
def login():
    if trigger_first_time() and User.query.count() == 0:
        return redirect("/first_time")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = authenticate(username, password)
        if not user:
            return render_template("login.html", username=username, msg="Try again.")

        # login and validate the user...
        login_user(user)
        # flash("Logged in successfully.")
        return redirect(request.args.get("next") or "/")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
