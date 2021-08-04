from flask_restful import Resource, reqparse, abort
from flask_login import login_user, login_required, logout_user, current_user


from models import Product
from config import db

parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("price", type=float)
parser.add_argument("stock", type=int)
parser.add_argument("category", type=int)


class AllProductResource(Resource):
    @login_required
    def get(self):
        products = Product.query.all()
        return [product.serialize() for product in products]


    def post(self):
        try:
            args = parser.parse_args(strict=True)
            product = Product()
            product.name = args["name"]
            product.price = args["price"]
            product.stock = args["stock"]
            product.category = args["category"]
            db.session.add(product)
            db.session.commit()
            return product.serialize(), 201
        except Exception as e:
            return abort(400, message="Some arguements are missing.")