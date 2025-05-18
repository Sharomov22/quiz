from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, FieldList, IntegerField
from wtforms.validators import DataRequired


class NewRoomForm(FlaskForm):
    only_authorized = BooleanField('Впускать только авторизованных?')
    template = SelectField('Квиз', validators=[DataRequired()])
    password = StringField('Пароль')
    assessment = FieldList(IntegerField('Оценка'), min_entries=4)
    submit = SubmitField('Создать')
