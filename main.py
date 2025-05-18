from flask import Flask, render_template, redirect, request
from data import db_session
from forms.login_form import LoginForm
from forms.room_form import RoomForm
from forms.register_form import RegisterForm
from forms.new_quiz_form import NewQuizForm
from data.users import User
from data.rooms import Rooms
from data.quiz_templates import Quiz_templates
from flask_login import login_user, LoginManager, logout_user, login_required, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key22'


def main():
    db_session.global_init("db/quiz.db")

    @app.route('/')
    @app.route('/index')
    def index():
        form = RoomForm()
        if form.validate_on_submit():
            return redirect(f'/room{form.password}')
        return render_template('index.html', form=form)

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
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            error_answer = ''
            if form.password.data != form.password_again.data:
                error_answer = 'Пароли не совпадают'
            else:
                db_sess = db_session.create_session()
            if not error_answer and db_sess.query(User).filter(User.login == form.login.data).first():
                error_answer = "Такой пользователь уже есть"
            if len(form.password.data) > 32 or len(form.login.data) > 32 or len(form.nickname.data) > 32:
                error_answer = "Превышен лимит в 32 символа на строку"
            if len(form.password.data) < 8:
                error_answer = "Пароль должен быть длинной не менее 8 символов"
            if error_answer:
                return render_template('register.html', form=form, message=error_answer)
            user = User(
                nickname=form.nickname.data,
                login=form.login.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', form=form)

    @app.route('/new_quiz', methods=['GET', 'POST'])
    @login_required
    def new_quiz():
        form = NewQuizForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            quiz = Quiz_templates()
            quiz.title = form.title.data
            quiz.content = form.content.data
            current_user.quiz.append(quiz)
            db_sess.merge(current_user)
            db_sess.commit()
            for question in form.content.data:
                if len(set(i for i in question["answer"])) != len([i for i in question["answer"]]):
                    return render_template('new_quiz.html',
                                           message='Варианты ответа должны отличаться', form=form)
                else:
                    pass
        return render_template('new_quiz.html', form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
