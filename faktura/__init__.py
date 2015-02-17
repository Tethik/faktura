from flask import Flask, request, render_template, send_file, redirect, make_response

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

import faktura.models
import faktura.invoice
import faktura.settings
import faktura.customer
