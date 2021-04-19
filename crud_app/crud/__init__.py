from flask import Blueprint

from crud_app.crud import views

crud = Blueprint('crud', __name__)
