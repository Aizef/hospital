from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import db_session
from data.models.users import User
from data.models.news import New
from data.models.appointments import Appointment
from forms.news import NewsForm
from forms.user import LoginForm, RegisterForm
from forms.appointment import AppointmentForm
from test import default_test
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html")


@app.errorhandler(403)
def not_found(e):
    return render_template("errors/403.html")


@app.errorhandler(401)
def not_found(e):
    return render_template("errors/401.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess = db_session.create_session()
        form = LoginForm()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(New).filter(
            (New.user == current_user) | (New.is_private != True))
    else:
        news = db_sess.query(New).filter(New.is_private != True)
    return render_template("index.html", news=news)

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(New).filter(New.id == id,
                                         New.user == current_user
                                         ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(New).filter(New.id == id,
                                         New.user == current_user
                                         ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/appointments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointments(id):
    form = AppointmentForm()
    db_sess = db_session.create_session()
    doctors = db_sess.query(User).filter(User.post_id == 2)
    form.doctor.choices = list(map(lambda x: x.name, doctors))
    if request.method == "GET":
        db_sess = db_session.create_session()
        appointments = db_sess.query(Appointment).filter(Appointment.id == id,
                                         Appointment.user == current_user
                                         ).first()
        if appointments:
            form.date.data = appointments.date.strftime('%Y-%m-%d')
            form.time.data = appointments.time.strftime('%H:%M:%S')
            form.doctor.data = appointments.doctor
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        appointments = db_sess.query(Appointment).filter(Appointment.id == id,
                                         Appointment.user == current_user
                                         ).first()
        if appointments:
            appointments.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
            appointments.time = datetime.strptime(form.time.data, '%H:%M:%S').time()
            appointments.doctor = form.doctor.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('appointment.html',
                           title='Изменение записи',
                           form=form
                           )

@app.route('/appointments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def appointments_delete(id):
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.id == id, Appointment.user == current_user).first()
    if appointments:
        db_sess.delete(appointments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/history')

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(New).filter(New.id == id, New.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = New()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)

@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    form = AppointmentForm()
    db_sess = db_session.create_session()
    doctors = db_sess.query(User).filter(User.post_id == 2)
    form.doctor.choices = list(map(lambda x: x.name, doctors))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        appointments = Appointment()
        appointments.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        appointments.time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        appointments.doctor = form.doctor.data
        appointments.user_id = current_user.id
        db_sess.add(appointments)
        db_sess.commit()
        return redirect('/')
    return render_template('appointment.html', title='Запись к врачу',
                           form=form)

@app.route("/history")
def history():
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.user_id == current_user.id)
    appointments = [i for i in appointments]
    return render_template('history.html', title='История записей',
                           appointments=appointments)


def main():
    db_session.global_init("db/blogs.db")
    default_test(db_session)
    app.run()


if __name__ == '__main__':
    main()
