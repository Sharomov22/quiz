from flask import Flask, render_template, redirect
from data import db_session
from forms.loginform import  LoginForm
from forms.roomform import  RoomForm
from forms.registerform import RegisterForm
from data.users import User

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

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == form.login.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                nickname=form.nickname.data,
                login=form.login.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()