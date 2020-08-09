from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):

    mail = StringField("Почта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    submit = SubmitField('Вход в систему')


class RegistrationForm(FlaskForm):
    mail = StringField("Почта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class ChangeForm(FlaskForm):
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть не менее 8 символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые")
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")


class OrderForm(FlaskForm):
    name = StringField('Ваше имя:', [InputRequired(message="Введите что-нибудь")])
    address = StringField('Вас адрес:', [InputRequired(message="Введите что-нибудь")])
    phone = StringField('Ваш телефон:', [InputRequired(message="Введите что-нибудь")])
