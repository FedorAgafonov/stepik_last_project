from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    order_details = db.relationship("OrderDetail")
    orders = db.relationship("Order")


class OrderDetail(db.Model):
    __tablename__ = 'orders_details'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")

    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"))
    meal = db.relationship("Meal")

    unique_id = db.Column(db.String, db.ForeignKey("orders.unique_num"))
    unique = db.relationship("Order")

    count = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    sum = db.Column(db.Float)
    status = db.Column(db.String)
    date = db.Column(db.String)
    unique_num = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")

    orders = db.relationship("OrderDetail")


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categorys.id"))
    category = db.relationship("Category")

    orders_details = db.relationship("OrderDetail")


class Category(db.Model):
    __tablename__ = 'categorys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    meal = db.relationship("Meal")
