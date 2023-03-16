from flask import Blueprint

example_blueprint = Blueprint('example_blueprint', __name__)
example2_blueprint = Blueprint('example2_blueprint', __name__)

@example_blueprint.route('/')
def index():
    return "This is an example app"

@example2_blueprint.route('/test')
def index():
    return "This is an example app3"
