from faktura import app
from flask import request, render_template, send_file, redirect, make_response
from faktura.breadcrumbs import breadcrumbs

@app.route('/settings')
def settings():
    return render_template('settings.html', breadcrumbs=breadcrumbs("Main Menu"))
