from faktura import app
from flask import request, render_template, redirect
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from faktura.models import db, User
from passlib.hash import sha256_crypt

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

def create_user(username, password):
    user = User()
    user.username = username
    user.password = sha256_crypt.encrypt(password)

    db.session.add(user)
    db.session.commit()


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return user
    if sha256_crypt.verify(password, user.password):
        return user
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
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
