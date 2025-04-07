from flask import Flask
from data.error_handlers import not_found, not_found_2, not_found_3
from data import db_session
from data.models.users import User
from db.db_fill import db_fill
from flask_login import LoginManager
from routes.main_routes import bp as main_bp
from api import patient_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(main_bp)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, not_found_2)
    app.register_error_handler(401, not_found_3)
    db_session.global_init("db/database.db")
    db_fill(db_session)
    app.register_blueprint(patient_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
