from faktura import app
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from faktura.models import db

if __name__ == "__main__":
    cfg_file = os.getcwd() + "/faktura.cfg"
    print(cfg_file)

    app.debug = True
    app.config.from_pyfile(cfg_file)

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    print(db.engine)
    manager.run()
