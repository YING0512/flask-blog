from flask_wtf import FlaskForm # 導入 FlaskForm 類別，用於創建表單
from flask_wtf.file import FileField, FileAllowed #導入 FileField 和 FileAllowed，用於處理文件上傳
from flask_login import current_user #導入 current_user，來獲取當前登入的使用者
from wtforms import StringField, PasswordField, SubmitField, BooleanField # 從 wtforms 模組導入各種欄位類型
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # 導入 ValidationError 類別，用來處理表單驗證錯誤
from flaskblog.models import User # 導入 User 類別，用來操作使用者資料

# 註冊表單類別
class RegistrationForm(FlaskForm):
    # 使用者名稱欄位，要求輸入並限制字數範圍
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 電子郵件欄位，要求輸入並進行郵箱格式驗證
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼欄位，要求輸入
    password = PasswordField('Password', validators=[DataRequired()])
    # 確認密碼欄位，要求輸入並驗證是否與密碼一致
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # 提交按鈕
    submit = SubmitField('Sign Up')

    # 驗證使用者名稱是否已被註冊
    def validate_username(self, username):
        # 查詢資料庫中是否已經有相同的使用者名稱
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已被註冊
    def validate_email(self, email):
        # 查詢資料庫中是否已經有相同的電子郵件
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# 登錄表單類別
class LoginForm(FlaskForm):
    # 電子郵件欄位
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼欄位
    password = PasswordField('Password', validators=[DataRequired()])
    # 記住我欄位
    remember = BooleanField('Remember Me')
    # 提交按鈕
    submit = SubmitField('Login')


# 更新帳戶表單類別
class UpdateAccountForm(FlaskForm):
    # 使用者名稱欄位
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 電子郵件欄位
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 更新頭像欄位，允許上傳圖片格式為 jpg 或 png
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # 提交按鈕
    submit = SubmitField('Update')

    # 驗證使用者名稱是否已被註冊
    def validate_username(self, username):
        # 如果使用者名稱有變更，檢查資料庫中是否已經有相同的使用者名稱
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已被註冊
    def validate_email(self, email):
        # 如果電子郵件有變更，檢查資料庫中是否已經有相同的電子郵件
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
