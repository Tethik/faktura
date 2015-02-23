from faktura import app
from faktura.models import db
import os
from faktura.auth import create_user



app.config.from_pyfile(os.getcwd() + "/faktura.cfg")
db.create_all()

# create_user("tethik", "password")

app.run()
