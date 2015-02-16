from faktura import app
from flask import request, render_template, send_file, redirect, make_response

@app.route('/customers')
def customers():
    return render_template('customers.html')
