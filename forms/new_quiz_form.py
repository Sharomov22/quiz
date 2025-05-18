from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField
from wtforms import  SubmitField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    class Meta:
        csrf = False
    question = StringField('Вопрос', validators=[DataRequired()])
    answer = FieldList(StringField('Ответ', validators=[DataRequired()]), min_entries=4)

class NewQuizForm(FlaskForm):
    title = StringField('Название викторины', validators=[DataRequired()])
    content = FieldList(FormField(QuizForm), min_entries=1)
    submit = SubmitField('Применить')
