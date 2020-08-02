from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    adres = db.Column(db.String, nullable=False)

    order = db.relationship("Order")


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    summa = db.Column(db.Integer)
    status = db.Column(db.String)
    mail = db.Column(db.String)
    phone = db.Column(db.String)
    adres = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")

    package = db.relationship("Package")


class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    order = db.relationship("Order")

    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"))
    meal = db.relationship("Meal")


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categorys.id"))
    category = db.relationship("Category")


class Category(db.Model):
    __tablename__ = 'categorys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    meal = db.relationship("Meal")
