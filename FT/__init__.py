from flask import Flask

#Create a Flask Instance
app = Flask(__name__)

import FT.views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)