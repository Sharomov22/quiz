from flask import Flask, render_template, redirect
from data import db_session
from loginform import  LoginForm
from roomform import  RoomForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/quiz.db")

    @app.route('/')
    @app.route('/index')
    def index():
        form = RoomForm()
        if form.validate_on_submit():
            return redirect('/success')
        return render_template('index.html', title='Главная', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            return redirect('/success')
        return render_template('login.html', title='Авторизация', form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()