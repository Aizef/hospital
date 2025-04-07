from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user

from data import db_session
from data.models.doctors import Doctor
from data.models.users import User
from forms.user import LoginForm, RegisterForm

bp = Blueprint('main', __name__)


@bp.route('/register', methods=['GET', 'POST'])
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


@bp.route('/login', methods=['GET', 'POST'])
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


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@bp.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("main.html")


@bp.route("/doctors")
def doctors():
    specialty = request.args.get('specialty')
    shift_0 = [(p, k) for p in range(24) for k in range(5) if p < 12]
    shift_1 = [(p, k) for p in range(24) for k in range(5) if p >= 12]
    db_sess = db_session.create_session()
    if not specialty:
        doctors = db_sess.query(Doctor).all()
    else:
        doctors = db_sess.query(Doctor).filter(Doctor.service_id == specialty)
    return render_template('doctors.html', title='История записей',
                           doctors=doctors, shift_0=shift_0, shift_1=shift_1)


@bp.route("/doctors/<int:id>")
def doctors_search(id):
    shift_0 = [(p, k) for p in range(24) for k in range(5) if p < 12]
    shift_1 = [(p, k) for p in range(24) for k in range(5) if p >= 12]
    db_sess = db_session.create_session()
    doctors = db_sess.query(Doctor).filter(Doctor.service_id == id).all()
    return render_template('doctors.html', title='История записей',
                           doctors=doctors, shift_0=shift_0, shift_1=shift_1)
