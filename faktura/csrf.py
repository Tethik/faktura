from faktura import app
from flask import session, request, abort
from Crypto import Random
import base64

rndfile = Random.new()

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = base64.b64encode(rndfile.read(32)).decode("ascii")
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token
