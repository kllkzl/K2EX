from flask import Blueprint,render_template


main = Blueprint('main', __name__)

from V2EX.main import views