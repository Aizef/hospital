from flask import Flask, abort
from data.error_handlers import *
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
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    # app.register_error_handler(402, payment_required)  # flask не поддерживает эту ошибку
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    # app.register_error_handler(407, proxy_auth_required)  # flask не поддерживает эту ошибку
    app.register_error_handler(408, request_timeout)
    app.register_error_handler(409, conflict)
    app.register_error_handler(410, gone)
    app.register_error_handler(411, length_required)
    app.register_error_handler(412, precondition_failed)
    app.register_error_handler(413, payload_too_large)
    app.register_error_handler(414, uri_too_long)
    app.register_error_handler(415, unsupported_media_type)
    app.register_error_handler(416, range_not_satisfiable)
    app.register_error_handler(417, expectation_failed)
    app.register_error_handler(418, im_a_teapot)
    app.register_error_handler(421, misdirected_request)
    app.register_error_handler(422, unprocessable_entity)
    app.register_error_handler(423, locked)
    app.register_error_handler(424, failed_dependency)
    # app.register_error_handler(425, too_early)  # flask не поддерживает эту ошибку
    # app.register_error_handler(426, upgrade_required)  # flask не поддерживает эту ошибку
    app.register_error_handler(428, precondition_required)
    app.register_error_handler(429, too_many_requests)
    app.register_error_handler(431, headers_too_large)
    app.register_error_handler(451, legal_unavailable)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(501, not_implemented)
    app.register_error_handler(502, bad_gateway)
    app.register_error_handler(503, service_unavailable)
    app.register_error_handler(504, gateway_timeout)
    app.register_error_handler(505, http_version_not_supported)
    # app.register_error_handler(506, variant_negotiates)  # flask не поддерживает эту ошибку
    # app.register_error_handler(507, insufficient_storage)  # flask не поддерживает эту ошибку
    # app.register_error_handler(508, loop_detected)  # flask не поддерживает эту ошибку
    # app.register_error_handler(510, not_extended)  # flask не поддерживает эту ошибку
    # app.register_error_handler(511, network_auth_required)  # flask не поддерживает эту ошибку
    db_session.global_init("db/database.db")
    db_fill(db_session)
    app.register_blueprint(patient_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
