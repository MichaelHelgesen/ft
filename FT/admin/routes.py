from flask import Blueprint

end = Blueprint('end', __name__)
test2 = Blueprint('test2', __name__)

@end.route('/end')
def index3():
    return "This is an example app2"

@test2.route('/test2')
def index4():
    return "This is an example app3"
