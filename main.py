from flask import Flask, render_template, redirect, request
from data import db_session
from forms.login_form import LoginForm
from forms.room_form import RoomForm
from forms.register_form import RegisterForm
from forms.new_quiz_form import NewQuizForm
from data.users import User
from flask_login import login_user, LoginManager, logout_user, login_required, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/quiz.db")

    @app.route('/')
    @app.route('/index')
    def index():
        form = RoomForm()
        if form.validate_on_submit():
            return redirect(f'/room{form.password}')
        return render_template('index.html', title='Главная', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.login == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect("/index")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
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
            if len(form.password) > 32 or len(form.login) > 32 or len(form.nickname) > 32:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Превышен лимит в 32 символа на строку")
            user = User(
                nickname=form.nickname.data,
                login=form.login.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/new_quiz', methods=['GET', 'POST'])
    @login_required
    def new_quiz():
        form = NewQuizForm()
        if request.method == 'POST':
            for number, type_ in zip(
                    request.form.getlist('question'),
                    request.form.getlist('answer')
            ):
                if number:
                    print(f'Phone number: {number} ({type_})')
        return render_template('new_quiz.html', title='Добавление викторины',
                               form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()