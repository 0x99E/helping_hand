from flask import Flask

import views
import models



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    global_db = models.db
    global_db.init_app(app)
    global_db.create_all(app=app)
    app.config['database'] = global_db
    with app.app_context():
        app.register_blueprint(views.user.blueprint)
        app.register_blueprint(views.task.blueprint)
        app.register_blueprint(views.telegram.blueprint)
        app.register_blueprint(views.auth.blueprint)
        

    return app