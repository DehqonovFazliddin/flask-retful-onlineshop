from flask_restful import Resource, reqparse
from flask_login import login_user, login_required, logout_user, current_user

from models import Category
from config import db

parser = reqparse.RequestParser()
parser.add_argument("name")


class AllCategoryResource(Resource):
    @login_required
    def get(self):
        categories = Category.query.all()
        return [category.serialize() for category in categories]
    
    def post(self):
        args = parser.parse_args()
        category = Category(name=args["name"])
        db.session.add(category)
        db.session.commit()
        return category.serialize()