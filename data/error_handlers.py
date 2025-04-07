from flask import render_template


def not_found(e):
    return render_template("errors/404.html")


def not_found_2(e):
    return render_template("errors/403.html")


def not_found_3(e):
    return render_template("errors/401.html")
