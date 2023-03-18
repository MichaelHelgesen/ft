from FT import app
from .login import routes as login
from .admin import routes as admin

app.register_blueprint(login.start)
app.register_blueprint(login.test)
app.register_blueprint(admin.end)
app.register_blueprint(admin.test2)