from faktura import app
import os

app.config.from_pyfile(os.getcwd() + "/faktura.cfg")
app.run()
