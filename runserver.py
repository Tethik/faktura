from faktura import app
from faktura.models import db
import os

app.config.from_pyfile(os.getcwd() + "/faktura.cfg")
db.create_all()
app.run()
