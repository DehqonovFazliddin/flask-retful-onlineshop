from config import app, api, db
from models import User
from flask_login import LoginManager

from api.category import *
from api.product import *
from api.cart import *


api.add_resource(AllCategoryResource, '/api/category/')
api.add_resource(SingleCategoryResource, '/api/category/<int:pk>/')

api.add_resource(AllProductResource, '/api/products/')
api.add_resource(SingleProductResource, '/api/product/<int:pk>/')

api.add_resource(AllCartResource, "/api/carts/")

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    app.run(debug=True)