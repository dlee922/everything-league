# Authentication and login routes
from flask import Blueprint
from app.services.auth_service import register_user, login_user

login_bp = Blueprint('login', __name__)
register_bp = Blueprint('register', __name__)
protected_bp = Blueprint('protected', __name__)


@login_bp.route('', methods=['POST'])
def login():
    return login_user()

@register_bp.route('',methods=['POST'])
def register():
    return register_user()
