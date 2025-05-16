from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    username = StringField('Отображаемое имя', validators=[DataRequired()])
    password = PasswordField('Тэг комнаты', validators=[DataRequired()])
    submit = SubmitField('Подключиться')
