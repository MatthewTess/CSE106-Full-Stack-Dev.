from flask import Blueprint
from flask_admin import Admin

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin' )

admin = Admin(admin_blueprint, name='Dashboard', template_mode='bootstrap3', url='/admin_dash')
