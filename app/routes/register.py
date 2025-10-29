from flask import Blueprint, render_template, request, redirect, url_for

register_bp = Blueprint("register", __name__)

@register_bp.route("/register_driver")
def register_driver():
    return render_template("register.html")


@register_bp.route("/register_passenger")
def register_passenger():
    return render_template("register.html")