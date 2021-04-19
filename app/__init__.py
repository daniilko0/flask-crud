from flask import Flask


def create_app():
    from app import models
    from crud import crud as crud_blueprint

    app = Flask(__name__)
    app.register_blueprint(crud_blueprint)

    return app
