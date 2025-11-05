from flask import Blueprint, render_template, request, redirect, url_for
import json

register_bp = Blueprint("register", __name__)

@register_bp.route("/register_driver", methods=["POST"])
def register_driver():
    if (request.method == "POST"):
        form_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'type': 'driver'
        }
        with open('drivers.json', 'a+') as f:
            json.dump(form_data, f)
            f.write('\n')
    return render_template("register.html")


@register_bp.route("/register_passenger", methods=["POST"])
def register_passenger():
    if (request.method == "POST"):
        form_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'type': 'passenger'
        }
        with open('passengers.json', 'a+') as f:
            json.dump(form_data, f)
            f.write('\n')
    return render_template("register.html")