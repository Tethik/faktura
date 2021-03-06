from faktura import app
from flask import request, render_template, send_file, redirect, make_response, jsonify
from faktura.breadcrumbs import breadcrumbs
from faktura.models import db, TemplateVariable, User
from flask.ext.login import login_required
from faktura.csrf import generate_csrf_token


@app.route('/settings')
@login_required
def settings():
    variables = TemplateVariable.query.all()
    users = User.query.all()
    return render_template('settings.html', variables=variables, users=users, breadcrumbs=breadcrumbs("Main Menu"))


@app.route('/vars/create', methods=['POST'])
@login_required
def create_var():
    var = TemplateVariable(request.form["key"], request.form["value"])
    db.session.add(var)
    db.session.commit()
    return jsonify(var=var.to_json(), _csrf_token=generate_csrf_token())

@app.route('/vars/save', methods=['POST'])
@login_required
def save_var():
    var = TemplateVariable.query.filter(TemplateVariable.key == request.form["key"]).first()
    var.value = request.form["value"]
    db.session.commit()
    return jsonify(var=var.to_json(),  _csrf_token=generate_csrf_token())

@app.route('/vars/delete', methods=['POST'])
@login_required
def delete_var():
    var = TemplateVariable.query.filter(TemplateVariable.key == request.form["key"]).first()
    db.session.delete(var)
    db.session.commit()
    return jsonify(var=var.to_json(),  _csrf_token=generate_csrf_token())
