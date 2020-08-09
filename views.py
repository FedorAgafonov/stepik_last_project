from flask import render_template, session, redirect, request, flash, url_for
import datetime
import random
import string
from collections import Counter
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from models import db, Category, Meal, User, OrderDetail, Order
from forms import LoginForm, RegistrationForm, OrderForm, ChangeForm


@app.route('/')
def render_main_page():

    cart = session.get("cart", {})
    products = {}
    for item in cart:
        products[db.session.query(Meal).filter(Meal.id == item).first()] = cart[item]
    summa = 0
    for prod in products:
        summa += int(prod.price) * int(products[prod])

    categories = db.session.query(Category.title, Category.id).all()
    clean_categories = []
    for category in categories:
        clean_categories.append(tuple(category))
    category_meal = {}
    for i in range(1, len(clean_categories) + 1):
        category_meal[i] = [item for item in db.session.query(Meal).filter(Meal.category_id == i).limit(3)]
    login = session.get('is_auth')
    return render_template("main.html", categories=clean_categories, meals=category_meal, is_auth=login, summa=summa, len=len(cart))


@app.route('/addtocart/<meal_id>', methods=["GET", "POST"])
def add_to_cart(meal_id):

    if request.method == "POST":

        username = request.form.get("number")
        cart = session.get("cart", {})
        cart[meal_id] = username
        session["cart"] = cart

    return redirect(url_for('render_main_page'))


@app.route('/deletefromcart/<int:meal_id>')
def delete_from_cart(meal_id):
    cart = session.get("cart", {})
    del cart[str(meal_id)]
    session["cart"] = cart
    return redirect(url_for('render_cart_page'))


@app.route('/cart/')
def render_cart_page():
    form = OrderForm()
    cart = session.get("cart", {})
    products = {}
    for item in cart:
        products[db.session.query(Meal).filter(Meal.id == item).first()] = cart[item]
    summa = 0
    for prod in products:
        summa += int(prod.price) * int(products[prod])
    login = session.get('is_auth')
    return render_template("cart.html", products=products, summa=summa,  is_auth=login, form=form)


@app.route('/categories/<category_id>/')
def render_categories_page(category_id):

    cart = session.get("cart", {})
    products = {}
    for item in cart:
        products[db.session.query(Meal).filter(Meal.id == item).first()] = cart[item]
    summa = 0
    for prod in products:
        summa += int(prod.price) * int(products[prod])

    category = db.session.query(Category).filter(Category.id == category_id).first()
    product_category = db.session.query(Meal).filter(Meal.category_id == category_id).all()
    login = session.get('is_auth')
    return render_template('categories.html', categories=category, product_category=product_category, is_auth=login, summa=summa, len=len(cart))


@app.route('/account/')
def render_account_page():
    orders = db.session.query(Order).filter(Order.user_id == session.get('user_id')).all()
    details = {}
    for item in orders:
        details[item.unique_num] = db.session.query(OrderDetail.count, Meal.title, Meal.price * OrderDetail.count).join(Meal).filter(db.and_(OrderDetail.unique_id == item.unique_num, OrderDetail.meal_id == Meal.id)).all()
    login = session.get('is_auth')
    return render_template("account.html", is_auth=login, orders=orders, details=details)


@app.route('/addtodb/<int:summa>', methods=["GET", "POST"])
def add_to_db(summa):
    form = OrderForm()
    if session['cart']:
        if request.method == 'POST':
            name = form.name.data
            phone = form.phone.data
            address = form.address.data

            cart = Counter(session.get('cart', []))
            now = datetime.datetime.now().strftime('%d-%m-%Y')

            unique = str(session.get('user_id')) + random.choice(string.ascii_letters) + str(random.randint(1, 999))
            order = Order(unique_num=unique, sum=summa, status='accepted', date=now, user_id=session.get('user_id'), address=address, phone=phone, name=name)
            db.session.add(order)

            for item in cart:
                detail = OrderDetail(user_id=session.get('user_id'), meal_id=item, unique_id=unique, count=cart[item])
                db.session.add(detail)

            db.session.commit()
            session.pop('cart')
            if session.get('is_auth'):
                return redirect(url_for('render_ordered_page'))
            return redirect(url_for('render_main_page'))
    return redirect(url_for('render_cart_page'))


@app.route('/login/', methods=["GET", "POST"])
def render_login_page():
    error_msg = ""
    form = LoginForm()
    if request.method == 'POST':
        mail = form.mail.data
        password = form.password.data
        get_user = db.session.query(User).filter(User.mail == mail).first()
        if get_user and check_password_hash(get_user.password, password):
            session['is_auth'] = True
            session['user_id'] = get_user.id
            return redirect(url_for('render_main_page'))
        else:
            error_msg = "Неверное имя пользователя или пароль"
    return render_template("login.html", form=form, error_msg=error_msg)


@app.route('/register/', methods=["GET", "POST"])
def render_register_page():
    form = RegistrationForm()
    error_msg = ""
    if request.method == 'POST':
        mail = form.mail.data
        password = form.password.data

        get_user_mail = db.session.query(User).filter(User.mail == mail).first()
        if get_user_mail:
            error_msg = "Пользователь уже существует"
        else:
            user = User(mail=mail, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            session['is_auth'] = True
            session['user_id'] = db.session.query(User.id).filter(User.mail == mail).first()[0]
            return redirect(url_for('render_main_page'))

    return render_template("register.html", form=form, error_msg=error_msg)


@app.route('/logout/')
def render_logout_page():
    if session.get("is_auth"):
        session.pop("is_auth")
        session.pop("user_id")
    return redirect(url_for('render_login_page'))


@app.route('/profile/', methods=["GET", "POST"])
def render_profile_page():

    cart = session.get("cart", {})
    products = {}
    for item in cart:
        products[db.session.query(Meal).filter(Meal.id == item).first()] = cart[item]
    summa = 0
    for prod in products:
        summa += int(prod.price) * int(products[prod])

    form = ChangeForm()
    error_msg = ""

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(id=session.get('user_id')).first()
            user.password = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash(f"Ваш пароль изменён")

    user = db.session.query(User).filter(User.id == session.get('user_id')).first()
    login = session.get('is_auth')
    return render_template("profile.html", form=form, is_auth=login, user=user, error_msg=error_msg, summa=summa, len=len(cart))


@app.route('/ordered/')
def render_ordered_page():
    return render_template('ordered.html')
