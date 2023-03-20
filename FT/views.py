from FT import app
from .login import routes as login
from .page import routes as page
from .models.add_test import Test


app.register_blueprint(page.page)
app.register_blueprint(login.login)
app.register_blueprint(login.forgot_password)