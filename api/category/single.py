from flask_restful import Resource, reqparse, abort


from models import Category
from config import db

parser = reqparse.RequestParser()
parser.add_argument("name")


class SingleCategoryResource(Resource):
    def patch(self, pk):
        args = parser.parse_args()
        categories = Category.query.filter_by(id=pk)
        if not categories.count() == 0:
            category = categories.first()
            category.name = args["name"]
            db.session.commit()
            return category.serialize(), 201
        else:
            return abort(404, message="Requested category is not found.")

    def delete(self, pk):
        categories = Category.query.filter_by(id=pk)
        if not categories.count() == 0:
            category = categories.first()
            db.session.delete(category)
            db.session.commit()
            return "", 204
        else:
            return abort(404, message="Requested category is not found.")
