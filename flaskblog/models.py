from datetime import datetime # 導入 datetime 類別，用於處理日期和時間
from flaskblog import db, login_manager # 導入 db 和 login_manager，這是 SQLAlchemy 的實例
from flask_login import UserMixin # 導入 UserMixin 類別，這是一個混入類，用來支援登入管理功能


# 設定用戶加載方法，這個方法會在用戶登入時被呼叫
@login_manager.user_loader
def load_user(user_id):
    # 根據 user_id 查詢並返回對應的用戶資料
    return User.query.get(int(user_id))


# 定義 User 類別，表示使用者的資料模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 用戶唯一識別 ID
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名，唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件，唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 用戶頭像檔案名稱，預設為 default.jpg
    password = db.Column(db.String(60), nullable=False)  # 密碼，長度為 60，且不可為空
    posts = db.relationship('Post', backref='author', lazy=True)  # 與 Post 類別的關聯，一個用戶可有多篇文章

    # 用於打印用戶物件的顯示方式
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# 定義 Post 類別，表示文章的資料模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 文章唯一識別 ID
    title = db.Column(db.String(100), nullable=False)  # 文章標題，長度為 100，且不可為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 文章發佈日期，預設為當前時間
    content = db.Column(db.Text, nullable=False)  # 文章內容，不可為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外鍵，關聯到 User 類別的 id

    # 用於打印文章物件的顯示方式
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
