from flask import render_template
from app import app


@app.route('/')
def render_main_page():
    return render_template("main.html")


@app.route('/cart/')
def render_portfolio_page():
    return render_template("cart.html")


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

