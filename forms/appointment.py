from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from datetime import datetime, date, time, timedelta


def add_time(t, delta):
    date = datetime(1, 1, 1)
    dt = datetime.combine(date, t)
    result = dt + delta
    return result.time()


class AppointmentServiceForm(FlaskForm):
    service = SelectField("Специальность", choices=[], validators=[DataRequired()])
    submit = SubmitField('Применить')


class AppointmentDoctorForm(FlaskForm):
    doctor = SelectField("Врач", choices=[], validators=[DataRequired()])
    submit = SubmitField('Применить')


class AppointmentDatetimeForm(FlaskForm):
    dates = [datetime.now().date() + (i + 1) * timedelta(days=1) for i in range(14)]
    dates = [i for i in dates if i.weekday() not in (5, 6)]
    times = [add_time(time(8), i * timedelta(minutes=30)) for i in range(24)]
    date = SelectField("Дата приёма", choices=dates, validators=[DataRequired()])
    time = SelectField("Время приёма", choices=times, validators=[DataRequired()])
    submit = SubmitField('Применить')