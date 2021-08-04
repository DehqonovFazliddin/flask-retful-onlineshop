from flask_restful import Resource, reqparse
from flask_login import login_user, login_required, logout_user, current_user

from models import Cart
from config import db

parser = reqparse.RequestParser()
parser.add_argument("name")


class AllCartResource(Resource):
    @login_required
    def get(self):
        carts = Cart.query.all()
        return [cart.serialize() for cart in carts]
    
    def post(self):
        args = parser.parse_args()
        cart = Cart(name=args["name"])
        db.session.add(cart)
        db.session.commit()
        return cart.serialize()