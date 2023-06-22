from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender_interest = db.Column(db.String(10), nullable=True)
    interest1_id = db.Column(db.Integer, db.ForeignKey('interest.id'))
    interest2_id = db.Column(db.Integer, db.ForeignKey('interest.id'))
    interest3_id = db.Column(db.Integer, db.ForeignKey('interest.id'))
    interest4_id = db.Column(db.Integer, db.ForeignKey('interest.id'))

    interest1 = db.relationship('Interest', foreign_keys=[interest1_id])
    interest2 = db.relationship('Interest', foreign_keys=[interest2_id])
    interest3 = db.relationship('Interest', foreign_keys=[interest3_id])
    interest4 = db.relationship('Interest', foreign_keys=[interest4_id])


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(10), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='likes')
    liked_user = db.relationship('User', foreign_keys=[liked_user_id], backref='liked_by')


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='login')


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matchA_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    matchB_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(10), nullable=False)

    matchA = db.relationship('User', foreign_keys=[matchA_id], backref='matchA')
    matchB = db.relationship('User', foreign_keys=[matchB_id], backref='matchB')




class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)

    from_user = db.relationship('User', foreign_keys=[from_id], backref='sent_messages')
    to_user = db.relationship('User', foreign_keys=[to_id], backref='received_messages')


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_name = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='pictures')
