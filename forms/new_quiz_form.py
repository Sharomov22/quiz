from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField
from wtforms import  SubmitField
from wtforms.validators import DataRequired


class PhoneForm(FlaskForm):
    class Meta:
        csrf = False  # это подформа, csrf не нужен
    question = StringField('Вопрос', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])

class NewQuizForm(FlaskForm):
    title = StringField('Название викторины', validators=[DataRequired()])
    questions = FieldList(FormField(PhoneForm), min_entries=1)
    submit = SubmitField('Применить')
