from flask import render_template, session, redirect, request, flash
import datetime
import random
import string
from collections import Counter
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from models import db, Category, Meal, User, OrderDetail, Order
from forms import LoginForm, RegistrationForm, ChangeForm


@app.route('/')
def render_main_page():
    categories = db.session.query(Category.title, Category.id).all()
    clean_categories = []
    for category in categories:
        clean_categories.append(tuple(category))
    category_meal = {}
    for i in range(1, len(clean_categories) + 1):
        category_meal[i] = [item for item in db.session.query(Meal).filter(Meal.category_id == i).limit(3)]
    login = session.get('is_auth')
    return render_template("main.html", categories=clean_categories, meals=category_meal, is_auth=login)


@app.route('/addtocart/<meal_id>')
def add_to_cart(meal_id):

    cart = session.get("cart", [])
    cart.append(int(meal_id))
    session["cart"] = cart
    return redirect('/cart/')


@app.route('/deletefromcart/<int:meal_id>')
def delete_from_cart(meal_id):
    cart = session.get("cart", [])
    meal_index = cart.index(meal_id)
    cart.pop(meal_index)
    session["cart"] = cart
    return redirect('/cart/')


@app.route('/cart/')
def render_cart_page():
    cart = session.get("cart", [])
    products = []
    for meal in cart:
        products.append(db.session.query(Meal).filter(Meal.id == meal).first())
    summa = 0
    count = 0
    for item in Counter(products):
        count += Counter(products)[item]
        summa += Counter(products)[item] * int(item.price)
    login = session.get('is_auth')
    return render_template("cart.html", count=count, products=Counter(products), summa=summa, is_auth=login)


@app.route('/categories/<category_id>/')
def render_categories_page(category_id):
    category = db.session.query(Category).filter(Category.id == category_id).first()
    product_category = db.session.query(Meal).filter(Meal.category_id == category_id).all()
    login = session.get('is_auth')
    return render_template('categories.html', categories=category, product_category=product_category, is_auth=login)


@app.route('/account/')
def render_account_page():
    orders = db.session.query(Order).filter(Order.user_id == session.get('user_id')).all()
    details = {}
    for item in orders:
        details[item.unique_num] = db.session.query(OrderDetail.count, Meal.title, Meal.price * OrderDetail.count).join(Meal).filter(db.and_(OrderDetail.unique_id == item.unique_num, OrderDetail.meal_id == Meal.id)).all()
    login = session.get('is_auth')
    return render_template("account.html", is_auth=login, orders=orders, details=details)


@app.route('/addtodb/<int:summa>')
def add_to_db(summa):
    if session['cart']:
        cart = Counter(session.get('cart', []))
        now = datetime.datetime.now().strftime('%d-%m-%Y')

        unique = str(session.get('user_id')) + random.choice(string.ascii_letters) + str(random.randint(1, 999))
        order = Order(unique_num=unique, sum=summa, status='accepted', date=now, user_id=session.get('user_id'))
        db.session.add(order)

        for item in cart:
            detail = OrderDetail(user_id=session.get('user_id'), meal_id=item, unique_id=unique, count=cart[item])
            db.session.add(detail)

        db.session.commit()
        session.pop('cart')
        return redirect('/account/')
    else:
        return redirect('/cart/')


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
            return redirect('/')
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
        phone = form.phone.data
        town = form.town.data
        street = form.street.data
        building = form.building.data
        flat = form.flat.data
        get_user_mail = db.session.query(User).filter(User.mail == mail).first()
        get_user_phone = db.session.query(User).filter(User.phone == phone).first()
        if get_user_mail or get_user_phone:
            error_msg = "Пользователь уже существует"
        else:
            user = User(mail=mail, password=generate_password_hash(password), phone=phone, town=town, street=street, building=building, flat=flat)
            db.session.add(user)
            db.session.commit()
            session['is_auth'] = True
            session['user_id'] = db.session.query(User.id).filter(User.mail == mail).first()[0]
            return redirect('/')

    return render_template("register.html", form=form, error_msg=error_msg)


@app.route('/logout/')
def render_logout_page():
    if session.get("is_auth"):
        session.pop("is_auth")
        session.pop("user_id")
        if session.pop('cart', []):
            session.pop('cart')
    return redirect("/login")


@app.route('/profile/', methods=["GET", "POST"])
def render_profile_page():
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
    return render_template("profile.html", form=form, is_auth=login, user=user, error_msg=error_msg)

