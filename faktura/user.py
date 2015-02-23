from faktura import app
from flask import render_template, request
from faktura.models import db, User
from faktura.breadcrumbs import breadcrumbs
from flask.ext.login import login_required
from passlib.hash import sha256_crypt

@app.route("/user/<int:user_id>", methods=["POST", "GET"])
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    msg = ""
    if request.method == "POST":
        if request.form["action"] == "details":
            user.email = request.form["email"]
            db.session.commit()
            msg = "Changed email successfully."
        elif request.form["action"] == "changepassword":
            user = User.query.filter_by(id=user_id).first()
            if not sha256_crypt.verify(request.form["old_password"], user.password):
                msg = "Old password did not match."
            elif request.form["new_password"] != request.form["rep_password"]:
                msg = "New and repeated password do not match."
            else:
                user.password = sha256_crypt.encrypt(request.form["new_password"])
                msg = "Password changed."
                db.session.commit()

    return render_template("users/show.html", user=user, msg=msg, breadcrumbs=breadcrumbs("Main Menu", "Settings"))
