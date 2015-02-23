from flask import Flask, request, render_template, send_file, redirect, make_response
from flask.ext.login import login_required, current_user

app = Flask(__name__)


import faktura.models
import faktura.auth
import faktura.invoice
import faktura.settings
import faktura.customer
import faktura.csrf

@app.route('/')
@login_required
def hello():
    return render_template("index.html", current_user=current_user)
