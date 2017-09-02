from flask import Flask
from .models import db



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    from .views import first_blueprint
    app.register_blueprint(first_blueprint)
    db.init_app(app)
    with app.app_context():
        return app
