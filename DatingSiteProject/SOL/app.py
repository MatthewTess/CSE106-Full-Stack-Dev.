import datetime
import os
import sqlite3
from functools import wraps

from flask import Flask, render_template, send_from_directory, session, request, redirect, flash, url_for, abort
from flask_admin import Admin
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from model import Interest, Like, Login, Match, Message, Picture, User, db
from views import InterestModelView, UserModelView, LikeModelView, LoginModelView, MatchModelView, MessageModelView, \
    PictureModelView, CustomAdminIndexView
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static/img/profile'
db_name = './instance/sol.db'
db.init_app(app)
with app.app_context():
    db.create_all()

admin = Admin(app, name='SOL Admin', template_mode='bootstrap4', index_view=CustomAdminIndexView())

# Register the custom views with the admin
admin.add_view(InterestModelView(Interest, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(LikeModelView(Like, db.session))
admin.add_view(LoginModelView(Login, db.session))
admin.add_view(MatchModelView(Match, db.session))
admin.add_view(MessageModelView(Message, db.session))
admin.add_view(PictureModelView(Picture, db.session))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/profile_picture/<int:user_id>')
def profile_picture(user_id):
    return send_from_directory(directory='static/img/profile', path=f'{user_id}.jpg')


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def home():  # put application's code here

    return render_template('home.html')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    interests = Interest.query.all()
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        gender_interest = request.form['gender_interest']
        interest1 = Interest.query.get(request.form['interest1'])
        interest2 = Interest.query.get(request.form['interest2'])
        interest3 = Interest.query.get(request.form['interest3'])
        interest4 = Interest.query.get(request.form['interest4'])
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            flash('Passwords do not match.')
            return render_template('signup.html', interests=interests)

        hashed_password = generate_password_hash(password, method='sha256')

        # Check and save the profile picture
        profile_picture = request.files['profile_picture']
        if profile_picture and allowed_file(profile_picture.filename):
            # Save the profile picture with the user's username as its filename
            file_extension = profile_picture.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{username}.{file_extension}")

            # Create the uploads directory if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(filepath)
        else:
            flash('Invalid profile picture. Please upload a JPEG file.')
            return render_template('signup.html', interests=interests)

        # Insert the new user into the database
        new_id = User.query.order_by(desc(User.id)).first()
        new_user = User(id=new_id.id + 1, name=name, gender=gender, dob=dob, email=email,
                        gender_interest=gender_interest, interest1=interest1, interest2=interest2,
                        interest3=interest3, interest4=interest4)
        db.session.add(new_user)
        new_login = Login(user_id=new_id.id + 1, user_name=username, password=hashed_password)
        db.session.add(new_login)
        db.session.commit()

        flash('You have successfully signed up!')
        return redirect(url_for('login'))
    return render_template('signup.html', interests=interests)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the user exists in the database
        username = request.form['username']
        password = request.form['password']

        user = Login.query.filter_by(user_name=username).first()
        if user and check_password_hash(user.password, password):
            # Save the user ID in the session and redirect to the home page
            session['id'] = user.user_id
            session['profilePic'] = str(user.user_id) + ".jpg"
            session['loggedIn'] = True
            session['username'] = username

            if user.user_id == 0:
                return redirect(url_for('admin.index'))

            return redirect(url_for('home'))
        else:
            # Show an error message if the login credentials are invalid
            flash('Invalid username or password.')
            if user:
                flash(user.password)
    return render_template('login.html')


@app.route('/logout')
def logout():  # put application's code here
    session.pop('id', None)
    session.pop('profilePic', None)
    session['loggedIn'] = False
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():  # put application's code here
    user_id = session['id']
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(
        f'SELECT * FROM login WHERE id  NOT IN (SELECT liked_user_id FROM like WHERE user_id = {user_id}) AND id != {user_id};')
    user_data = cur.fetchall()
    if user_data is None:
        user_data = []

    session['users'] = user_data
    con.close()
    return render_template('profile/feed.html')


@app.route('/sendmessage/<int:to>', methods=['GET', 'POST'])
@login_required
def sendmessage(to):
    if request.method == 'POST':
        message_text = request.form['message']
        from_id = session['id']

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        message = Message(from_id=from_id, to_id=to, message=message_text, date=date, time=time)
        db.session.add(message)
        db.session.commit()

    from_id = session['id']
    messages = db.session.query(Message, User).filter(
        User.id == Message.to_id,
        (Message.from_id == from_id) & (Message.to_id == to) | (Message.from_id == to) & (Message.to_id == from_id)
    ).all()

    return render_template('profile/sendmessage.html', messages=messages, to=to)


@app.route('/message', methods=['GET'])
@login_required
def message():
    user_id = session['id']

    matched_users = User.query.join(Match, (User.id == Match.matchA_id) | (User.id == Match.matchB_id)).filter(
        ((Match.matchA_id == user_id) | (Match.matchB_id == user_id)) & (User.id != user_id)
    ).all()

    session['users'] = [(user.id, user.email, user.name) for user in matched_users]

    return render_template('profile/messages.html')


@app.route('/likes', methods=['GET', 'POST'])
@login_required
def likes():  # put application's code here
    user_id = session['id']
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(
        f'SELECT * FROM login WHERE id  IN (SELECT user_id FROM like WHERE liked_user_id = {user_id}) AND id != {user_id};')
    user_data = cur.fetchall()
    if user_data is None:
        user_data = []

    session['users'] = user_data
    con.close()
    return render_template('profile/likes.html')


@app.route('/like/<int:user_id>', methods=['GET', 'POST'])
@login_required
def like(user_id):
    liked_user = User.query.filter_by(id=user_id).first()
    if liked_user is None:
        return redirect(url_for('likes'))

    # Check if the user has already liked the liked_user
    existing_like = Like.query.filter_by(user_id=session['id'], liked_user_id=user_id).first()

    if existing_like is None:
        # Create a new like
        new_like = Like(user_id=session['id'], liked_user_id=user_id)
        db.session.add(new_like)
        db.session.commit()

        # Check if the liked_user has also liked the user
        reverse_like = Like.query.filter_by(user_id=user_id, liked_user_id=session['id']).first()

        if reverse_like is not None:
            # If it's a mutual like, create a new match
            match = Match(matchA_id=session['id'], matchB_id=user_id, date=datetime.now())
            db.session.add(match)
            db.session.commit()

    return redirect(url_for('likes'))



@app.route('/matches', methods=['GET'])
@login_required
def matches():
    match_user_id = session['id']

    matched_users = User.query.join(Match, (User.id == Match.matchA_id) | (User.id == Match.matchB_id)).filter(
        ((Match.matchA_id == match_user_id) | (Match.matchB_id == match_user_id)) & (User.id != match_user_id)
    ).all()

    session['match_users'] = [(user.id, user.email, user.name) for user in matched_users]

    return render_template('profile/matches.html')


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))

    return render_template('profile/profile.html', user=user)


@app.route('/my_likes')
@login_required
def my_likes():  # put application's code here
    user_id = session['id']
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'SELECT * FROM login WHERE id IN (SELECT liked_user_id FROM like WHERE user_id = {user_id});')
    user_data = cur.fetchall()
    if user_data is None:
        user_data = []

    session['users'] = user_data

    con.close()
    return render_template('profile/my_likes.html')


@app.route('/unlike/<int:user_id>')
@login_required
def unlike(user_id):
    like = Like.query.filter_by(user_id=session.get('id'), liked_user_id=user_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('You have unliked this user.', 'success')
    else:
        flash('You have not liked this user.', 'error')
    return redirect(url_for('my_likes'))


@app.route('/delete')
@login_required
def delete():  # put application's code here
    return render_template('profile/delete.html')


if __name__ == '__main__':
    app.run()
