# GROUP: Aakash Koirala,  Matthews Tessema and Ariana Curtis


from flask import Flask, render_template, request, url_for, redirect, session
from flask import flash
from sqlalchemy import desc
from flask_admin import BaseView, expose

from admin_dash import admin_blueprint

from forms import LoginForm, StudentRegistrationForm, AdminRegistration, DeleteStudentForm, DeleteTeacherForm, \
    TeacherRegistrationForm, AddClassForm, RemoveClassForm, UpdateStudentGradeForm, DropClassForm, RegisterClassForm

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models import db, Student, User, Teacher, Admin, Class, Enrollment


class AdminDashView(BaseView):
    @expose('/')
    def index(self):
        if session.get('logged_in') and session.get('user_role') == 'admin':
            return self.render('admin/admin_dash.html')
        else:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ntu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(admin_blueprint)
with app.app_context():
    db.create_all()


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        flash('You are already logged in.', 'info')
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin'))
        if session.get('user_role') == 'student':
            return redirect(url_for('student'))
        if session.get('user_role') == 'teacher':
            return redirect(url_for('teacher'))
    form = LoginForm()
    if form.validate_on_submit():
        user_to_login = User.query.filter_by(username=form.username.data).first()
        if user_to_login and check_password_hash(user_to_login.password, form.password.data):
            session['logged_in'] = True
            session['user_role'] = user_to_login.role
            session['id'] = user_to_login.id
            flash('Logged in successfully.', 'success')
            if user_to_login.role == 'admin':
                info = Admin.query.filter_by(id=user_to_login.id).first()
                session['name'] = info.name
                return redirect(url_for('admin'))
            if user_to_login.role == 'student':
                info = Student.query.filter_by(id=user_to_login.id).first()
                session['name'] = info.name
                return redirect(url_for('student'))
            if user_to_login.role == 'teacher':
                info = Teacher.query.filter_by(id=user_to_login.id).first()
                session['name'] = info.name
                return redirect(url_for('student'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    admins = Admin.query.order_by(Admin.id).all()
    form = AdminRegistration()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.lastName.data, method='sha256')
        id_admin = User.query.filter_by(role='admin').order_by(desc(User.id)).first()
        new_log_in = User(id=id_admin.id + 1, username=form.firstName.data, password=hashed_password, role='admin')
        new_admin = Admin(id=id_admin.id + 1, name=(form.firstName.data + " " + form.lastName.data))
        db.session.add(new_log_in)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin registered successfully.', 'success')
        return redirect(url_for('register_admin'))
    return render_template('admin/register_admin.html', form=form, admins=admins)


# add teacher

@app.route('/admin')
def admin():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    classes = Class.query.order_by(Class.id).all()
    return render_template('admin/dashboard.html', classes=classes)


@app.route('/all_grades')
def all_grades():
    if session.get('logged_in') and session.get('user_role') == 'admin':
        enrollments = Enrollment.query.join(Student, Student.id == Enrollment.student_id).join(Class,
                                                                                               Class.id == Enrollment.class_id).join(
            Teacher, Teacher.id == Class.teacher_id).order_by(Enrollment.id).all()

        return render_template('admin/all_grades.html', enrollments=enrollments)
    flash('Please log in first.', 'warning')
    return redirect(url_for('login'))


@app.route('/manage_enrollments', methods=['GET', 'POST'])
def manage_enrollments():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form.get('action')
        enrollment_id = request.form.get('enrollment_id')
        grade = request.form.get('grade')

        if action == 'add':
            student_id = request.form.get('student_id')
            class_id = request.form.get('class_id')
            target_class = Class.query.get(class_id)

            if target_class.capacity > target_class.enrolled:
                target_class.enrolled += 1
                new_enrollment = Enrollment(student_id=student_id, class_id=class_id)
                db.session.add(new_enrollment)
                db.session.commit()
            else:
                flash("The class is already full. Please select another class.", "error")

        elif action == 'delete':
            enrollment = Enrollment.query.get(enrollment_id)
            target_class = Class.query.get(enrollment.class_id)
            target_class.enrolled -= 1
            db.session.delete(enrollment)
            db.session.commit()

        elif action == 'update':
            enrollment = Enrollment.query.get(enrollment_id)
            enrollment.grade = grade
            db.session.commit()

    enrollments = Enrollment.query.join(Student, Student.id == Enrollment.student_id).join(Class,
                                                                                           Class.id == Enrollment.class_id).join(
        Teacher, Teacher.id == Class.teacher_id).order_by(Enrollment.id).all()
    students = Student.query.all()
    classes = Class.query.all()
    return render_template('admin/manage_enrollments.html', enrollments=enrollments, students=students, classes=classes)


@app.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    teachers = Teacher.query.order_by(Teacher.name).all()

    form = AddClassForm()
    form.teacher_id.choices = [(teacher.id, f"{teacher.name} (ID: {teacher.id})") for teacher in teachers]
    if form.validate_on_submit():
        id_class = Class.query.order_by(desc(Class.id)).first()
        new_class = Class(id=id_class.id + 1, class_name=form.class_name.data, teacher_id=form.teacher_id.data,
                          time=form.time.data,
                          capacity=form.capacity.data, enrolled=0)
        db.session.add(new_class)
        db.session.commit()
        flash('Class added successfully.', 'success')
        return redirect(url_for('add_class'))
    classes = Class.query.order_by(Class.id).all()
    return render_template('admin/add_class.html', form=form, classes=classes)


@app.route('/remove_class', methods=['GET', 'POST'])
def remove_class():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    form = RemoveClassForm()
    form.class_id.choices = [
        (class_item.id, f"ID: {class_item.id}, Name: {class_item.class_name}, Teacher: {class_item.teacher.name}") for
        class_item in Class.query.all()]

    if form.validate_on_submit():
        class_to_remove = Class.query.get(form.class_id.data)
        db.session.delete(class_to_remove)
        db.session.commit()
        flash('Class removed successfully.', 'success')
        return redirect(url_for('admin'))
    classes = Class.query.order_by(Class.id).all()
    return render_template('admin/delete_class.html', form=form, classes=classes)


@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    students = Student.query.order_by(Student.id).all()
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.lastName.data, method='sha256')
        id_student = User.query.filter_by(role='student').order_by(desc(User.id)).first()
        student_login = User(id=id_student.id + 1, username=form.firstName.data, password=hashed_password,
                             role='student')

        new_student = Student(id=id_student.id + 1, name=(form.firstName.data + " " + form.lastName.data))
        db.session.add(student_login)
        db.session.add(new_student)
        db.session.commit()
        flash('Student registered successfully.', 'success')
        return redirect(url_for('register_student'))
    return render_template('admin/register_student.html', form=form, students=students)


@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    form = DeleteStudentForm()
    students = Student.query.order_by(Student.id).all()
    form.student_id.choices = [(student.id, f"{student.name} (ID: {student.id})") for student in students]
    if form.validate_on_submit():
        student_to_delete = User.query.get(form.student_id.data)
        student_login_to_delete = Student.query.get(form.student_id.data)
        db.session.delete(student_to_delete)
        db.session.delete(student_login_to_delete)
        db.session.commit()
        flash('Student deleted successfully.', 'success')
        return redirect(url_for('delete_student'))

    return render_template('admin/delete_student.html', form=form, students=students)


@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    teachers = Teacher.query.order_by(Teacher.id).all()
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.lastName.data, method='sha256')
        id_teacher = User.query.filter_by(role='teacher').order_by(desc(User.id)).first()
        teacher_login = User(id=id_teacher.id + 1, username=form.firstName.data, password=hashed_password,
                             role='teacher')

        new_teacher = Teacher(id=id_teacher.id + 1, name=(form.firstName.data + " " + form.lastName.data))
        db.session.add(teacher_login)
        db.session.add(new_teacher)
        db.session.commit()
        flash('Teacher registered successfully.', 'success')
        return redirect(url_for('register_teacher'))
    return render_template('admin/register_teacher.html', form=form, teachers=teachers)


@app.route('/teacher')
def teacher():
    if session.get('logged_in') and session.get('user_role') == 'teacher':
        return render_template('teacher/dashboard.html')
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))


@app.route('/delete_teacher', methods=['GET', 'POST'])
def delete_teacher():
    if not session.get('logged_in') or session.get('user_role') != 'admin':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    teachers = Teacher.query.order_by(Teacher.name).all()
    form = DeleteTeacherForm()
    form.teacher_id.choices = [(teacher.id, f"{teacher.name} (ID: {teacher.id})") for teacher in teachers]
    if form.validate_on_submit():
        teacher_to_delete = User.query.get(form.teacher_id.data)
        teacher_login_to_delete = Teacher.query.get(form.teacher_id.data)
        db.session.delete(teacher_to_delete)
        db.session.delete(teacher_login_to_delete)
        db.session.commit()
        flash('Teacher deleted successfully.', 'success')
        return redirect(url_for('delete_teacher'))

    return render_template('admin/delete_teacher.html', form=form, teachers=teachers)


@app.route('/student')
def student():
    if session.get('logged_in') and session.get('user_role') == 'student':
        enrollments = Enrollment.query.filter_by(student_id=session.get('id')).all()
        return render_template('student/dashboard.html', enrollments=enrollments)
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))


@app.route('/register_class', methods=['GET', 'POST'])
def register_class():
    if not session.get('logged_in') or session.get('user_role') != 'student':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    # get all classes
    classes = Class.query.all()
    enrollments = Enrollment.query.filter_by(student_id=session.get('id')).all()

    if request.method == 'POST':
        class_id = request.form.get('class_id')
        target_class = Class.query.get(class_id)

        # check if class has available spots
        if target_class.capacity > target_class.enrolled:
            # check if student is already enrolled in class
            enrollment = Enrollment.query.filter_by(student_id=session.get('id'), class_id=class_id).first()
            if not enrollment:
                target_class.enrolled += 1
                new_enrollment = Enrollment(student_id=session.get('id'), class_id=class_id)
                db.session.add(new_enrollment)
                db.session.commit()
                flash('Successfully enrolled in class!', 'success')
            else:
                flash('You are already enrolled in this class.', 'warning')
        else:
            flash('The class is already full. Please select another class.', 'error')

    return render_template('student/add_class.html', classes=classes, enrollments=enrollments)


@app.route('/drop', methods=['GET', 'POST'])
def drop():
    if not session.get('logged_in') or session.get('user_role') != 'student':
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

        # handle drop request
    if request.method == 'POST':
        enrollment_id = request.form.get('enrollment_id')
        enrollment = Enrollment.query.get(enrollment_id)
        target_class = Class.query.get(enrollment.class_id)
        target_class.enrolled -= 1
        db.session.delete(enrollment)
        db.session.commit()
        flash("Class dropped successfully!", "success")

        # get currently registered classes
    enrollments = Enrollment.query.filter_by(student_id=session.get('id')).all()
    classes = []
    for enrollment in enrollments:
        classes.append(Class.query.get(enrollment.class_id))
    return render_template('student/drop.html', classes=classes)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_role', None)
    session.pop('id', None)
    session.pop('name', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


# matt

@app.route('/classes')
def classes():
    if session.get('logged_in') and session.get('user_role') == 'teacher':

        current_teacher = Teacher.query.get(session.get('id'))
        teacher_classes = Class.query.filter_by(teacher_id=session.get('id')).all()
        return render_template('teacher/classes.html', teacher_classes=teacher_classes, teacher=current_teacher.name)

    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))


@app.route('/classes/<class_id>')
def class_info(class_id):
    # students list that enrolled in this class
    students = Enrollment.query.filter_by(class_id=class_id).all()
    class_name = Class.query.filter_by(id=class_id).first()
    return render_template('teacher/class_detail.html', class_id=class_id, students=students, class_name=class_name)


@app.route('/update/<class_id>/<student_id>', methods=['GET', 'POST'])
def update_grade(class_id, student_id):
    form = UpdateStudentGradeForm()
    if form.validate_on_submit():
        Enrollment.query.filter_by(student_id=student_id).update(dict(grade=form.data["grade"]))
        db.session.commit()
        flash('Grade updated successfully.', 'success')
        return redirect(f'/classes/{class_id}')

    return render_template('teacher/update_grade.html', form=form)


@app.route('/delete/<class_id>/<student_id>')
def delete_from_class(class_id, student_id):
    student_to_delete = Enrollment.query.filter_by(student_id=student_id).first()
    db.session.delete(student_to_delete)
    db.session.commit()
    return redirect(f'/classes/{class_id}')


# matt


if __name__ == '__main__':
    app.run(debug=True)
