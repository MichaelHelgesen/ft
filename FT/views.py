from FT import app
from .login import routes as login
from .page import routes as page
from .projects import routes as projects
from .apartments import routes as apartments
from .products import routes as products
from .product_collections import routes as collections


app.register_blueprint(page.page)
app.register_blueprint(login.login)
app.register_blueprint(projects.projects)
app.register_blueprint(apartments.apartments)
app.register_blueprint(products.products)
app.register_blueprint(collections.product_col)