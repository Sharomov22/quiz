from flask import Flask, render_template, redirect, request, abort
from data import db_session
from forms.login_form import LoginForm
from forms.room_form import RoomForm
from forms.register_form import RegisterForm
from forms.new_quiz_form import NewQuizForm, QuizForm
from data.users import User
from data.rooms import Rooms
from forms.new_room_form import NewRoomForm
from data.quiz_templates import Quiz_templates
from flask_login import login_user, LoginManager, logout_user, login_required, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key22'


def main():
    db_session.global_init("db/quiz.db")

    # Главная
    @app.route('/')
    @app.route('/index')
    def index():
        form = RoomForm()
        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            quizes = db_sess.query(Quiz_templates).filter(Quiz_templates.user == current_user)
            return render_template('index.html', form=form, templates=quizes)
        if form.validate_on_submit():
            return redirect(f'/room{form.password}')
        return render_template('index.html', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    # Выход из аккаунта
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    # Авторизация
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

    # Регистрация
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

    # Создание квиза
    @app.route('/new_quiz', methods=['GET', 'POST'])
    @login_required
    def new_quiz():
        form = NewQuizForm()
        # Привет от костыля для редакции, там я объяснил, зачем это нужно
        form_to_default(form)
        if form.validate_on_submit():
            for question in form.content.data:
                if len(set(i for i in question["answer"])) != len([i for i in question["answer"]]):
                    return render_template('quiz_redactor.html',
                                           message='Варианты ответа должны отличаться', form=form)
                else:
                    db_sess = db_session.create_session()
                    quiz = Quiz_templates()
                    quiz.title = form.title.data
                    quiz.content = form.content.data
                    quiz.user = current_user
                    # иначе с сеансами беда, когда объект подключен к другому сеансу
                    quiz_for_db = db_sess.merge(quiz)
                    db_sess.add(quiz_for_db)
                    db_sess.commit()
                    return redirect('/')
        return render_template('quiz_redactor.html', form=form)

    # Редактирование квиза
    @app.route('/quiz/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_quiz(id):
        form = NewQuizForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            quiz = db_sess.query(Quiz_templates).filter(Quiz_templates.id == id,
                                                        Quiz_templates.user == current_user
                                                        ).first()
            if quiz:
                form.title.data = quiz.title
                # В самом FieldList нет сеттера, поэтому мне пришлось костыльным способом это делать через изменение стандартной формы
                form_to_default(form)
                form.content.pop_entry()
                for question in quiz.content:
                    form.content.append_entry(question)
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            quiz = db_sess.query(Quiz_templates).filter(Quiz_templates.id == id,
                                                        Quiz_templates.user == current_user).first()
            if quiz:
                for question in form.content.data:
                    if len(set(i for i in question["answer"])) != len([i for i in question["answer"]]):
                        return render_template(f'quiz/{id}.html',
                                               message='Варианты ответа должны отличаться', form=form)
                    else:
                        quiz.title = form.title.data
                        quiz.content = form.content.data
                        print(form.content.data)
                        db_sess.commit()
                        # Вот здесь я чищу форму до стандартной, чтобы потом при создании нового квиза, были пустые поля
                        form_to_default(form)
                        return redirect('/')
            else:
                abort(404)
        return render_template('quiz_redactor.html', form=form)

    # Удаление квиза
    @app.route('/quiz_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def news_delete(id):
        db_sess = db_session.create_session()
        quiz = db_sess.query(Quiz_templates).filter(Quiz_templates.id == id,
                                                    Quiz_templates.user == current_user).first()
        if quiz:
            db_sess.delete(quiz)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')

    # Настройка создаваемой комнаты
    @app.route('/host_room', methods=['GET', 'POST'])
    @login_required
    def new_room():
        form = NewRoomForm()
        db_sess = db_session.create_session()
        form.template.choices = [quiz.title for quiz in
                                 db_sess.query(Quiz_templates).filter(Quiz_templates.user == current_user)]
        if not form.template.choices:
            return redirect('/new_quiz')
        if form.validate_on_submit():
            pass
        return render_template('start_room.html', form=form)

    # Функция, которая возвращает форме начальный вид, после костыля для редакции
    def form_to_default(form):
        while form.content:
            form.content.pop_entry()
        form.content.append_entry({'question': None, 'answer': [None, None, None, None]})

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
