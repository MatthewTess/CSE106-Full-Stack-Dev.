from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db, Student, Class, Teacher, Enrollment, User


def init_admin(app):
    admin = Admin(app, name='NovaTech University Admin', template_mode='bootstrap3', url='/myadmin')

    # Add model views
    admin.add_view(ModelView(Student, db.session))
    admin.add_view(ModelView(Class, db.session))
    admin.add_view(ModelView(Teacher, db.session))
    admin.add_view(ModelView(Enrollment, db.session))
    admin.add_view(ModelView(User, db.session))


