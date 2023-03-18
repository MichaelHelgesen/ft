from flask import Blueprint

start = Blueprint('start', __name__)
test = Blueprint('test', __name__)

@start.route('/')
def index():
    return "This is an example app2"

@test.route('/test')
def index2():
    return "This is an example app3"
