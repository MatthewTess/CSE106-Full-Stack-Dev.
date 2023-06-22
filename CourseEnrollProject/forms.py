from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import IntegerField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class StudentRegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=64)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Register Student')


class AdminRegistration(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=64)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Register Admin')


class TeacherRegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=3, max=64)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=64)])
    submit = SubmitField('Register Teacher')


class DeleteStudentForm(FlaskForm):
    student_id = SelectField('Select Student', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Delete Student')


class DeleteTeacherForm(FlaskForm):
    teacher_id = SelectField('Select Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Delete Teacher')


class AddClassForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired(), Length(min=3, max=64)])
    teacher_id = SelectField('Select Teacher', coerce=int, validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired(), Length(min=3, max=64)])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    submit = SubmitField('Add Class')


class RemoveClassForm(FlaskForm):
    class_id = SelectField('Class ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Remove Class')


class UpdateStudentGradeForm(FlaskForm):
    grade = IntegerField('Grade', validators=[DataRequired()])
    submit = SubmitField('Update')


class DropClassForm(FlaskForm):
    enrollment_id = SelectField('Select Class', coerce=int)
    submit = SubmitField('Drop Class')


class RegisterClassForm(FlaskForm):
    class_id = SelectField('Select Class', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Class')
