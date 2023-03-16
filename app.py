import routes
from flask import Flask, render_template, redirect
from views import example_blueprint, example2_blueprint

#Create a Flask Instance
app = Flask(__name__)
app.register_blueprint(example_blueprint)
app.register_blueprint(example2_blueprint)

'''
app.add_url_rule('/', view_func=routes.index)
app.add_url_rule('/other', view_func=routes.other)
'''

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)