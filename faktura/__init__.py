from flask import Flask, request, render_template, send_file, redirect, make_response

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

import faktura.invoice
import faktura.settings
import faktura.customer




if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run()
