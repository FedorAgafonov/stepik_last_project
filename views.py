from flask import render_template, session, redirect
import datetime
from collections import Counter
from app import app
from models import db, Category, Meal, User


@app.route('/')
def render_main_page():
    categories = db.session.query(Category.title, Category.id).all()
    clean_categories = []
    for category in categories:
        clean_categories.append(tuple(category))
    category_meal = {}
    for i in range(1, len(clean_categories) + 1):
        category_meal[i] = [item for item in db.session.query(Meal).filter(Meal.category_id == i).limit(3)]
    return render_template("main.html", categories=clean_categories, meals=category_meal)


@app.route('/addtocart/<meal_id>')
def add_to_cart(meal_id):

    cart = session.get("cart", [])
    cart.append(meal_id)
    session["cart"] = cart

    return redirect('/cart/')


@app.route('/deletefromcart/<int:meal_id>')
def delete_from_cart(meal_id):
    cart = session.get("cart", [])
    meal_index = cart.index(str(meal_id))
    cart.pop(meal_index)
    session["cart"] = cart
    return redirect('/cart/')


@app.route('/cart/')
def render_portfolio_page():
    cart = session.get("cart", [])
    products = []
    for meal in cart:
        products.append(db.session.query(Meal).filter(Meal.id == meal).first())
    summa = 0
    count = 0
    for item in Counter(products):
        count += Counter(products)[item]
        summa += Counter(products)[item] * int(item.price)
    return render_template("cart.html", count=count, products=Counter(products), summa=summa)


@app.route('/categories/<category_id>/')
def render_categories_page(category_id):
    category = db.session.query(Category).filter(Category.id == category_id).first()
    product_category = db.session.query(Meal).filter(Meal.category_id == category_id).all()
    return render_template('categories.html', categories=category, product_category=product_category)


@app.route('/account/')
def render_certificates_page():
    return render_template("account.html")


@app.route('/login/')
def render_login_page():
    return render_template("login.html")


@app.route('/register/')
def render_register_page():
    return render_template("register.html")


@app.route('/logout/')
def render_logout_page():
    return render_template("logout.html")


@app.route('/ordered/')
def render_ordered_page():
    return render_template("ordered.html")

