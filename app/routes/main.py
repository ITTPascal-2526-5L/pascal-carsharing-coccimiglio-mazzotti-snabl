from flask import render_template, redirect, Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def homepage():
    return render_template("index.html")