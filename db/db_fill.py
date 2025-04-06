from data.models.services import Service
from data.models.doctors import Doctor


def db_fill(db_session):
    db_sess = db_session.create_session()

    if not db_sess.query(Service).filter(Service.name == "Хирург").first():
        service = Service()
        service.name = "Хирург"
        db_sess.add(service)
        db_sess.commit()
        doctor = Doctor()
        doctor.name = "Сидоров А.П."
        doctor.services = service
        doctor.shift = 0
        db_sess.add(doctor)
        doctor = Doctor()
        doctor.name = "Васильев Л.Д."
        doctor.services = service
        doctor.shift = 1
        db_sess.add(doctor)
    db_sess.commit()

    if not db_sess.query(Service).filter(Service.name == "Офтальмолог").first():
        service = Service()
        service.name = "Офтальмолог"
        db_sess.add(service)
        db_sess.commit()
        doctor = Doctor()
        doctor.name = "Петров Д.В."
        doctor.services = service
        doctor.shift = 0
        db_sess.add(doctor)
        doctor = Doctor()
        doctor.name = "Матвеев Г.М."
        doctor.services = service
        doctor.shift = 1
        db_sess.add(doctor)
    db_sess.commit()

    if not db_sess.query(Service).filter(Service.name == "Психолог").first():
        service = Service()
        service.name = "Психолог"
        db_sess.add(service)
        db_sess.commit()
        doctor = Doctor()
        doctor.name = "Иванов В.К."
        doctor.services = service
        doctor.shift = 0
        db_sess.add(doctor)
        doctor = Doctor()
        doctor.name = "Данилов Н.К."
        doctor.services = service
        doctor.shift = 1
        db_sess.add(doctor)
    db_sess.commit()

    if not db_sess.query(Service).filter(Service.name == "Стоматолог").first():
        service = Service()
        service.name = "Стоматолог"
        db_sess.add(service)
        db_sess.commit()
        doctor = Doctor()
        doctor.name = "Максимов А.М."
        doctor.services = service
        doctor.shift = 0
        db_sess.add(doctor)
        doctor = Doctor()
        doctor.name = "Дмитриев П.П."
        doctor.services = service
        doctor.shift = 1
        db_sess.add(doctor)
    db_sess.commit()

    if not db_sess.query(Service).filter(Service.name == "Терапевт").first():
        service = Service()
        service.name = "Терапевт"
        db_sess.add(service)
        db_sess.commit()
        doctor = Doctor()
        doctor.name = "Михайлов К.С."
        doctor.services = service
        doctor.shift = 0
        db_sess.add(doctor)
        doctor = Doctor()
        doctor.name = "Леонидов Р.В."
        doctor.services = service
        doctor.shift = 1
        db_sess.add(doctor)
    db_sess.commit()