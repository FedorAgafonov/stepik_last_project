from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, DataRequired


class LoginForm(FlaskForm):

    mail = StringField("Почта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    submit = SubmitField('Вход в систему')


class RegistrationForm(FlaskForm):
    mail = StringField("Почта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])

    phone = StringField('Телефон', [InputRequired(message="Введите что-нибудь")])
    town = StringField('Город', [InputRequired(message="Введите что-нибудь")])
    street = StringField('Улица', [InputRequired(message="Введите что-нибудь")])
    building = StringField('Дом', [InputRequired(message="Введите что-нибудь")])
    flat = StringField('Квартира', [InputRequired(message="Введите что-нибудь")])


class CountForm(FlaskForm):
    count = IntegerField('Количество товара', [InputRequired(message="Введите что-нибудь")])
