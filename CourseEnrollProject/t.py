from werkzeug.security import generate_password_hash

from main import User, db, app, Admin, Enrollment

with app.app_context():
    new_student = Enrollment(student_id='3000', class_id='0', grade='100')
    db.session.add(new_student)
    db.session.commit()
