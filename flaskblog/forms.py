from flask_wtf import FlaskForm # 匯入 FlaskForm
from flask_wtf.file import FileField, FileAllowed # 匯入 FileField 和 FileAllowed
from flask_login import current_user # 匯入 current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField # 匯入 StringField, PasswordField, SubmitField 和 BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # 匯入驗證器
from flaskblog.models import User # 匯入 User


class RegistrationForm(FlaskForm): # 建立 RegistrationForm 類別
    username = StringField('Username', # 建立 username 欄位
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', # 建立 email 欄位
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) # 建立 password 欄位
    confirm_password = PasswordField('Confirm Password', # 建立 confirm_password 欄位
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up') # 建立 submit 按鈕

    def validate_username(self, username): # 建立 validate_username 方法
        user = User.query.filter_by(username=username.data).first() # 查詢使用者
        if user: # 如果使用者存在
            raise ValidationError('That username is taken. Please choose a different one.') # 顯示錯誤訊息

    def validate_email(self, email): # 建立 validate_email 方法
        user = User.query.filter_by(email=email.data).first() # 查詢使用者
        if user: # 如果使用者存在
            raise ValidationError('That email is taken. Please choose a different one.') # 顯示錯誤訊息


class LoginForm(FlaskForm): # 建立 LoginForm 類別
    email = StringField('Email', # 建立 email 欄位
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) # 建立 password 欄位
    remember = BooleanField('Remember Me') # 建立 remember 欄位
    submit = SubmitField('Login') # 建立 submit 按鈕


class UpdateAccountForm(FlaskForm): # 建立 UpdateAccountForm 類別
    username = StringField('Username', # 建立 username 欄位
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', # 建立 email 欄位
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) # 建立 picture 欄位
    submit = SubmitField('Update') # 建立 submit 按鈕

    def validate_username(self, username): # 建立 validate_username 方法
        if username.data != current_user.username: # 如果使用者名稱不等於目前使用者名稱
            user = User.query.filter_by(username=username.data).first() # 查詢使用者
            if user: # 如果使用者存在
                raise ValidationError('That username is taken. Please choose a different one.') # 顯示錯誤訊息

    def validate_email(self, email): # 建立 validate_email 方法
        if email.data != current_user.email: # 如果電子郵件不等於目前電子郵件
            user = User.query.filter_by(email=email.data).first() # 查詢使用者
            if user: # 如果使用者存在
                raise ValidationError('That email is taken. Please choose a different one.') # 顯示錯誤訊息