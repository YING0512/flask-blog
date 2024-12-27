from flask import Flask # 從 flask 模組導入 Flask 類別
from flask_sqlalchemy import SQLAlchemy # 導入 SQLAlchemy 類別，用於資料庫操作
from flask_bcrypt import Bcrypt # 導入 Bcrypt 類別，用於加密密碼
from flask_login import LoginManager # 導入 LoginManager 類別，用於處理使用者登入管理

app = Flask(__name__) # 創建 Flask 應用實例

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # 設置應用的密鑰，用於加密會話資料
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 設定資料庫 URI，這裡使用 SQLite 資料庫
db = SQLAlchemy(app) # 創建 SQLAlchemy 實例，並將 Flask 應用傳遞給它
bcrypt = Bcrypt(app) # 創建 Bcrypt 實例，並將 Flask 應用傳遞給它，用於加密和檢查密碼
login_manager = LoginManager(app) # 創建 LoginManager 實例，並將 Flask 應用傳遞給它，用於管理使用者登入
login_manager.login_view = 'login' # 設置登入視圖，當用戶尚未登入時會重定向到這個視圖
login_manager.login_message_category = 'info' # 設置登入訊息的類別名稱，這將在登入頁面顯示提示信息

from flaskblog import routes # 從 flaskblog 模組導入路由，這樣可以初始化應用的路由配置
