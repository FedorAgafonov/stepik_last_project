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

    phone = StringField('Телефон:', [InputRequired(message="Введите что-нибудь")])
    town = StringField('Город:', [InputRequired(message="Введите что-нибудь")])
    street = StringField('Улица:', [InputRequired(message="Введите что-нибудь")])
    building = StringField('Дом:', [InputRequired(message="Введите что-нибудь")])
    flat = StringField('Квартира:', [InputRequired(message="Введите что-нибудь")])


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


class CountForm(FlaskForm):
    count = IntegerField('Количество товара', [InputRequired(message="Введите что-нибудь")])
