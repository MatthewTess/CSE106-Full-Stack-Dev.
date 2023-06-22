from flask import flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from models import User, Student, Teacher, Admin, Class, Enrollment
from models import db


class UserModelView(ModelView):
    column_list = ('id', 'username', 'role')
    column_exclude_list = ('password',)


class StudentModelView(ModelView):
    column_list = ('id', 'name', 'enrollments')


class TeacherModelView(ModelView):
    column_list = ('id', 'name', 'class_of_teacher')


class AdminUserModelView(ModelView):
    column_list = ('id', 'name')


class ClassModelView(ModelView):
    column_list = ('id', 'class_name', 'teacher', 'time', 'capacity', 'enrolled', 'enrollments')


class EnrollmentModelView(ModelView):
    column_list = ('id', 'student_id', 'class_id', 'grade')


# Add the views to the admin instance
from . import admin

admin.add_view(UserModelView(User, db.session))
admin.add_view(StudentModelView(Student, db.session))
admin.add_view(TeacherModelView(Teacher, db.session))
admin.add_view(AdminUserModelView(Admin, db.session))
admin.add_view(ClassModelView(Class, db.session))
admin.add_view(EnrollmentModelView(Enrollment, db.session))
