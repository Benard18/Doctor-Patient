from flask import Blueprint

main2 = Blueprint('main2',__name__)

from . import views,errors,forms
