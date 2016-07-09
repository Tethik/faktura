from flask import render_template
from faktura import app
from faktura.breadcrumbs import breadcrumbs

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', breadcrumbs=breadcrumbs("Main Menu")), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html', breadcrumbs=breadcrumbs("Main Menu")), 403

@app.errorhandler(500)
def page_server_error(e):
    return render_template('500.html', breadcrumbs=breadcrumbs("Main Menu")), 500
