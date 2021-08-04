from flask_restful import Resource, reqparse, abort

from models import Product
from config import db

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("price")
parser.add_argument("stock")
parser.add_argument("category")

class SingleProductResource(Resource):
    def patch(self, pk):
        args = parser.parse_args()
        product = Product.query.filter_by(id=pk)
        if not product.count() == 0:
            product = product.first()
            product.name = args["name"]
            product.price = args["price"]
            product.stock = args["stock"]
            product.category = args["category"]
            db.session.commit()
            return product.serialize(), 201
        else:
            return abort(404, message="Requested product is not found.")
