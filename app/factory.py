from flask import Flask
from flask_cors import CORS
import config
import views
import models



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile("config.py")
    global_db = models.db
    global_db.init_app(app)
    global_db.create_all(app=app)
    app.config['database'] = global_db

    

    with app.app_context():
        dbsettings_exists = bool(models.Config.query.first())
        if not dbsettings_exists:
            new_settings = models.Config()
            global_db.session.add(new_settings)
            global_db.session.commit()

        app.register_blueprint(views.user.blueprint)
        app.register_blueprint(views.task.blueprint)
        app.register_blueprint(views.telegram.blueprint)
        app.register_blueprint(views.auth.blueprint)
        

    return app