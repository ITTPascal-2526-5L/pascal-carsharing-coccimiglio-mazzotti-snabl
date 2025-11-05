from flask import Blueprint, render_template, request, redirect, url_for

register_bp = Blueprint("register", __name__)

@register_bp.route("/register_driver", methods=["POST"])
def register_driver():
    if (request.method == "POST"):
        print("POST")
    return render_template("register.html")


@register_bp.route("/register_passenger", methods=["POST"])
def register_passenger():
    if (request.method == "POST"):
        print("POST")
    return render_template("register.html")