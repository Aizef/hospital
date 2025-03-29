from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import db_session
from data.models.users import User
from data.models.services import Service
from data.models.doctors import Doctor
from data.models.appointments import Appointment
from forms.user import LoginForm, RegisterForm
from forms.appointment import AppointmentServiceForm, AppointmentDatetimeForm, AppointmentDoctorForm
from db.db_fill import db_fill
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
    return render_template("main.html")

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointments(id):
    form = AppointmentDatetimeForm()
    items = [i for i in form][:-2]
    if request.method == "GET":
        db_sess = db_session.create_session()
        appointments = db_sess.query(Appointment).filter(Appointment.id == id,
                                         Appointment.user == current_user
                                         ).first()
        if appointments:
            form.date.data = appointments.date.strftime('%Y-%m-%d')
            form.time.data = appointments.time.strftime('%H:%M:%S')
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
            db_sess.commit()
            return redirect('/history')
        else:
            abort(404)
    return render_template('appointment.html', title='Перенос записи', form=form, items=items)

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

@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment_service():
    form = AppointmentServiceForm()
    db_sess = db_session.create_session()
    form.service.choices = [i.name for i in db_sess.query(Service).all()]
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        session['appointment_data'] = {
            'service': form.service.data,
            'user_id': current_user.id
        }
        session.modified = True
        return redirect('/appointment_doctor')
    return render_template('appointment.html', title='Выбор специализации',
                           form=form, items=items)

@app.route('/appointment_doctor', methods=['GET', 'POST'])
@login_required
def appointment_doctor():
    form = AppointmentDoctorForm()
    db_sess = db_session.create_session()
    service = db_sess.query(Service).filter(Service.name == session['appointment_data']["service"]).first()
    form.doctor.choices = [i.name for i in db_sess.query(Doctor).filter(Doctor.service_id == service.id)]
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        session['appointment_data']["doctor"] = form.doctor.data
        session.modified = True
        return redirect('/appointment_datetime')
    return render_template('appointment.html', title='Выбор врача',
                           form=form, items=items)

@app.route('/appointment_datetime', methods=['GET', 'POST'])
@login_required
def appointment_datetime():
    form = AppointmentDatetimeForm()
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        appointments = Appointment()
        appointments.service = session['appointment_data']["service"]
        appointments.doctor = session['appointment_data']["doctor"]
        appointments.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        appointments.time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        appointments.user_id = current_user.id
        db_sess = db_session.create_session()
        db_sess.add(appointments)
        db_sess.commit()
        return redirect('/')
    return render_template('appointment.html', title='Выбор даты и времени приёма',
                           form=form, items=items)

@app.route('/appointment_datetime/<int:id>', methods=['GET', 'POST'])
@login_required
def appointment_datetime_1(id):
    form = AppointmentDatetimeForm()
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        appointments = Appointment()
        appointments.service = db_sess.query(Doctor).filter(Doctor.id == id).first().services.name
        appointments.doctor = db_sess.query(Doctor).filter(Doctor.id == id).first().name
        appointments.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        appointments.time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        appointments.user_id = current_user.id
        db_sess.add(appointments)
        db_sess.commit()
        return redirect('/')
    return render_template('appointment.html', title='Выбор даты и времени приёма',
                           form=form, items=items)


@app.route("/history")
def history():
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.user_id == current_user.id)
    appointments = [i for i in appointments]
    return render_template('history.html', title='История записей',
                           appointments=appointments)

@app.route("/doctors")
def doctors():
    db_sess = db_session.create_session()
    doctors = db_sess.query(Doctor).all()
    return render_template('doctors.html', title='История записей',
                           doctors=doctors)


def main():
    db_session.global_init("db/database.db")
    db_fill(db_session)
    app.run()


if __name__ == '__main__':
    main()
