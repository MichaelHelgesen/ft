from flask import Flask
#Create a Flask Instance
app = Flask(__name__)
app.secret_key = "hello"
import FT.views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)