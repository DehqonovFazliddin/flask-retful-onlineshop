from config import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def serialize(self):
        data = {
            "id": self.id,
            "name": f"{self.first_name} {self.last_name}",
            "phone": self.phone 
        }
        return data


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

    category = db.Column(db.Integer, db.ForeignKey("category.id"))

    def serialize(self):
        data = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

        category = Category.query.filter_by(id=int(self.category)).first()
        if category:
            data["category"] = category.serialize()

        return data



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_active = db.Column(db.Boolean, default=True)

    def serialize(self):
        data = {
            "id": self.id,
        }
        user = User.query.filter_by(id=int(self.user)).first()
        if user:
            data["user"] = user.serialize()

        


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean)


if __name__ == "__main__":
    db.create_all()