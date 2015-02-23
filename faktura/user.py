from faktura import app
from flask import render_template, request
from faktura.models import db, User
from faktura.breadcrumbs import breadcrumbs
from flask.ext.login import login_required

@app.route("/user/<int:user_id>", methods=["POST", "GET"])
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    msg = ""
    if request.method == "POST":
        user.email = request.form["email"]
        db.session.commit()
        msg = "Saved successfully."
    return render_template("users/show.html", user=user, msg=msg, breadcrumbs=breadcrumbs("Main Menu", "Settings"))
