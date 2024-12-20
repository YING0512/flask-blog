from flask import Flask # 匯入 Flask
from flask_sqlalchemy import SQLAlchemy # 匯入 SQLAlchemy
from flask_bcrypt import Bcrypt # 匯入 Bcrypt
from flask_login import LoginManager # 匯入 LoginManager

app = Flask(__name__) # 建立 Flask 實例
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # 設定 SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 設定資料庫 URI
db = SQLAlchemy(app) # 建立資料庫實例
bcrypt = Bcrypt(app) # 建立 Bcrypt 實例
login_manager = LoginManager(app) # 建立 LoginManager 實例
login_manager.login_view = 'login' # 設定登入頁面
login_manager.login_message_category = 'info' # 設定登入訊息分類

from flaskblog import routes # 匯入路由