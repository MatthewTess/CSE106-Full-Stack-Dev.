from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from model import Picture, User, Interest, Like, Login, Match, Message


class InterestModelView(ModelView):
    column_list = ('id', 'name')
    form_columns = ('id', 'name')


class UserModelView(ModelView):
    column_list = (
    'id', 'name', 'gender', 'dob', 'email', 'gender_interest', 'interest1_id', 'interest2_id', 'interest3_id',
    'interest4_id')
    form_columns = (
    'id', 'name', 'gender', 'dob', 'email', 'gender_interest', 'interest1', 'interest2', 'interest3', 'interest4')


class LikeModelView(ModelView):
    column_list = ('id', 'user_id', 'liked_user_id', 'date')
    form_columns = ('id', 'user', 'liked_user', 'date')


class LoginModelView(ModelView):
    column_list = ('id', 'user_id', 'user_name', 'password')
    form_columns = ('id', 'user', 'user_name', 'password')


class MatchModelView(ModelView):
    column_list = ('id', 'matchA_id', 'matchB_id', 'date')
    form_columns = ('id', 'matchA', 'matchB', 'date')


class MessageModelView(ModelView):
    column_list = ('id', 'from_id', 'to_id', 'message', 'date', 'time')
    form_columns = ('id', 'from_user', 'to_user', 'message', 'date', 'time')


class PictureModelView(ModelView):
    column_list = ('id', 'user_id', 'file_name')
    form_columns = ('id', 'user', 'file_name')


class CustomAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        user_count = User.query.count()
        interest_count = Interest.query.count()
        like_count = Like.query.count()
        login_count = Login.query.count()
        match_count = Match.query.count()
        message_count = Message.query.count()
        picture_count = Picture.query.count()

        return self.render(
            'admin/custom_index.html',
            user_count=user_count,
            interest_count=interest_count,
            like_count=like_count,
            login_count=login_count,
            match_count=match_count,
            message_count=message_count,
            picture_count=picture_count
        )
