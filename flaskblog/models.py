from datetime import datetime # 匯入datetime模組
from flaskblog import db, login_manager # 匯入db和login_manager
from flask_login import UserMixin # 匯入UserMixin


@login_manager.user_loader # 設定使用者載入器
def load_user(user_id): # 定義load_user函式
    return User.query.get(int(user_id)) # 回傳使用者


class User(db.Model, UserMixin): # 建立User類別
    id = db.Column(db.Integer, primary_key=True) # 建立id欄位
    username = db.Column(db.String(20), unique=True, nullable=False) # 建立username欄位
    email = db.Column(db.String(120), unique=True, nullable=False) # 建立email欄位
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # 建立image_file欄位
    password = db.Column(db.String(60), nullable=False) # 建立password欄位
    posts = db.relationship('Post', backref='author', lazy=True) # 建立posts欄位

    def __repr__(self): # 建立__repr
        return f"User('{self.username}', '{self.email}', '{self.image_file}')" # 回傳使用者名稱、電子郵件和圖片檔案名稱


class Post(db.Model): # 建立Post類別
    id = db.Column(db.Integer, primary_key=True) # 建立id欄位
    title = db.Column(db.String(100), nullable=False) # 建立title欄位
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # 建立date_posted欄位
    content = db.Column(db.Text, nullable=False) # 建立content欄位
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 建立user_id欄位

    def __repr__(self): # 建立__repr
        return f"Post('{self.title}', '{self.date_posted}')" # 回傳標題和發布日期