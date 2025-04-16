from flask import render_template


def bad_request(e):
    return render_template("errors/400.html")

def unauthorized(e):
    return render_template("errors/401.html")

def payment_required(e):
    return render_template("errors/402.html")

def forbidden(e):
    return render_template("errors/403.html")

def not_found(e):
    return render_template("errors/404.html")

def method_not_allowed(e):
    return render_template("errors/405.html")

def not_acceptable(e):
    return render_template("errors/406.html")

def proxy_auth_required(e):
    return render_template("errors/407.html")

def request_timeout(e):
    return render_template("errors/408.html")

def conflict(e):
    return render_template("errors/409.html")

def gone(e):
    return render_template("errors/410.html")

def length_required(e):
    return render_template("errors/411.html")

def precondition_failed(e):
    return render_template("errors/412.html")

def payload_too_large(e):
    return render_template("errors/413.html")

def uri_too_long(e):
    return render_template("errors/414.html")

def unsupported_media_type(e):
    return render_template("errors/415.html")

def range_not_satisfiable(e):
    return render_template("errors/416.html")

def expectation_failed(e):
    return render_template("errors/417.html")

def im_a_teapot(e):
    return render_template("errors/418.html")

def misdirected_request(e):
    return render_template("errors/421.html")

def unprocessable_entity(e):
    return render_template("errors/422.html")

def locked(e):
    return render_template("errors/423.html")

def failed_dependency(e):
    return render_template("errors/424.html")

def too_early(e):
    return render_template("errors/425.html")

def upgrade_required(e):
    return render_template("errors/426.html")

def precondition_required(e):
    return render_template("errors/428.html")

def too_many_requests(e):
    return render_template("errors/429.html")

def headers_too_large(e):
    return render_template("errors/431.html")

def legal_unavailable(e):
    return render_template("errors/451.html")

def internal_error(e):
    return render_template("errors/500.html")

def not_implemented(e):
    return render_template("errors/501.html")

def bad_gateway(e):
    return render_template("errors/502.html")

def service_unavailable(e):
    return render_template("errors/503.html")

def gateway_timeout(e):
    return render_template("errors/504.html")

def http_version_not_supported(e):
    return render_template("errors/505.html")

def variant_negotiates(e):
    return render_template("errors/506.html")

def insufficient_storage(e):
    return render_template("errors/507.html")

def loop_detected(e):
    return render_template("errors/508.html")

def not_extended(e):
    return render_template("errors/510.html")

def network_auth_required(e):
    return render_template("errors/511.html")
