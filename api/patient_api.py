from datetime import datetime

from flask import Blueprint, render_template, redirect, request, session, abort
from flask_login import login_required, current_user

from data import db_session
from data.models.appointments import Appointment
from data.models.doctors import Doctor
from data.models.services import Service
from data.models.appointments import Appointment
from forms.appointment import AppointmentDatetimeForm, AppointmentServiceForm, AppointmentDoctorForm

blueprint = Blueprint(
    'patient_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/api/history")
def history():
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.user_id == current_user.id)
    appointments = [i for i in appointments]
    return render_template('history.html', title='История записей',
                           appointments=appointments)


@blueprint.route('/api/edit_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointments(id):
    form = AppointmentDatetimeForm()
    items = [i for i in form][:-2]
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.doctor == session['appointment_data']["doctor"]).all()
    times = [(i.date, i.time) for i in appointments]
    shift = db_sess.query(Doctor).filter(Doctor.id == id).first().shift
    form.time.choices = form.times[0:12] if shift == 0 else form.times[12:24]
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
        date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        if (date, time) in times:
            return render_template('appointment.html', title='Перенос записи',
                                   form=form, items=items, message="На это время уже есть запись.")
        appointments = db_sess.query(Appointment).filter(Appointment.id == id,
                                                         Appointment.user == current_user
                                                         ).first()
        if appointments:
            appointments.date = date
            appointments.time = time
            db_sess.commit()
            return redirect('/api/history')
        else:
            abort(404)
    return render_template('appointment.html', title='Перенос записи', form=form, items=items)


@blueprint.route('/api/appointments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def appointments_delete(id):
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.id == id, Appointment.user == current_user).first()
    if appointments:
        db_sess.delete(appointments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/api/history')


@blueprint.route('/api/appointment', methods=['GET', 'POST'])
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
        return redirect('/api/appointment_doctor')
    return render_template('appointment.html', title='Выбор специализации',
                           form=form, items=items)


@blueprint.route('/api/appointment_doctor', methods=['GET', 'POST'])
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
        return redirect('/api/appointment_datetime')
    return render_template('appointment.html', title='Выбор врача',
                           form=form, items=items)


@blueprint.route('/api/appointment_datetime', methods=['GET', 'POST'])
@login_required
def appointment_datetime():
    form = AppointmentDatetimeForm()
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).filter(Appointment.doctor == session['appointment_data']["doctor"]).all()
    times = [(i.date, i.time) for i in appointments]
    shift = db_sess.query(Doctor).filter(Doctor.name == session['appointment_data']["doctor"]).first().shift
    form.time.choices = form.times[0:12] if shift == 0 else form.times[12:24]
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        if (date, time) in times:
            return render_template('appointment.html', title='Выбор даты и времени приёма',
                                   form=form, items=items, message="На это время уже есть запись.")
        appointments = Appointment()
        appointments.service = session['appointment_data']["service"]
        appointments.doctor = session['appointment_data']["doctor"]
        appointments.date = date
        appointments.time = time
        appointments.user_id = current_user.id
        db_sess = db_session.create_session()
        db_sess.add(appointments)
        db_sess.commit()
        return redirect('/')
    return render_template('appointment.html', title='Выбор даты и времени приёма',
                           form=form, items=items)


@blueprint.route('/api/appointment_datetime/<int:id>', methods=['GET', 'POST'])
@login_required
def appointment_datetime_doctor(id):
    form = AppointmentDatetimeForm()
    db_sess = db_session.create_session()
    doctor_name = db_sess.query(Doctor).filter(Doctor.id == id).first().name
    appointments = db_sess.query(Appointment).filter(Appointment.doctor == doctor_name).all()
    times = [(i.date, i.time) for i in appointments]
    shift = db_sess.query(Doctor).filter(Doctor.id == id).first().shift
    form.time.choices = form.times[0:12] if shift == 0 else form.times[12:24]
    items = [i for i in form][:-2]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        time = datetime.strptime(form.time.data, '%H:%M:%S').time()
        if (date, time) in times:
            return render_template('appointment.html', title='Выбор даты и времени приёма',
                                   form=form, items=items, message="На это время уже есть запись.")
        appointments = Appointment()
        appointments.service = db_sess.query(Doctor).filter(Doctor.id == id).first().services.name
        appointments.doctor = db_sess.query(Doctor).filter(Doctor.id == id).first().name
        appointments.date = date
        appointments.time = time
        appointments.user_id = current_user.id
        db_sess.add(appointments)
        db_sess.commit()
        return redirect('/')
    return render_template('appointment.html', title='Выбор даты и времени приёма',
                           form=form, items=items)
