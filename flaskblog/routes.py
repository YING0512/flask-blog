import os # 匯入 os 模組
import secrets # 匯入 secrets 模組
from PIL import Image # 匯入 Image 模組
from flask import render_template, url_for, flash, redirect, request # 匯入 render_template、url_for、flash、redirect 和 request
from flaskblog import app, db, bcrypt # 匯入 app、db 和 bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # 匯入 RegistrationForm、LoginForm 和 UpdateAccountForm
from flaskblog.models import User, Post # 匯入 User 和 Post
from flask_login import login_user, current_user, logout_user, login_required # 匯入 login_user、current_user、logout_user 和 login_required


posts = [ # 建立文章清單
    { # 第一篇文章
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    { # 第二篇文章
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/") # 設定路由
@app.route("/home") # 設定路由
def home(): # 定義 home 函式
    return render_template('home.html', posts=posts) # 回傳 home.html 模板和文章清單


@app.route("/about") # 設定路由
def about(): # 定義 about 函式
    return render_template('about.html', title='About') # 回傳 about.html 模板和標題


@app.route("/register", methods=['GET', 'POST']) # 設定路由
def register(): # 定義 register 函式
    if current_user.is_authenticated: # 如果使用者已經登入
        return redirect(url_for('home')) # 重新導向至主頁
    form = RegistrationForm() # 建立 RegistrationForm 表單
    if form.validate_on_submit(): # 如果表單驗證成功
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # 產生密碼雜湊
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # 建立使用者
        db.session.add(user) # 新增使用者
        db.session.commit() # 提交資料庫
        flash('Your account has been created! You are now able to log in', 'success') # 顯示訊息
        return redirect(url_for('login')) # 重新導向至登入頁面
    return render_template('register.html', title='Register', form=form) # 回傳 register.html 模板和標題


@app.route("/login", methods=['GET', 'POST']) # 設定路由
def login(): # 定義 login 函式
    if current_user.is_authenticated: # 如果使用者已經登入
        return redirect(url_for('home')) # 重新導向至主頁
    form = LoginForm() # 建立 LoginForm 表單
    if form.validate_on_submit(): # 如果表單驗證成功
        user = User.query.filter_by(email=form.email.data).first() # 查詢使用者
        if user and bcrypt.check_password_hash(user.password, form.password.data): # 如果使用者存在且密碼正確
            login_user(user, remember=form.remember.data) # 登入使用者
            next_page = request.args.get('next') # 取得下一頁面
            return redirect(next_page) if next_page else redirect(url_for('home'))  # 重新導向至下一頁面或主頁
        else: # 如果使用者不存在或密碼錯誤
            flash('Login Unsuccessful. Please check email and password', 'danger') # 顯示訊息
    return render_template('login.html', title='Login', form=form) # 回傳 login.html 模板和標題


@app.route("/logout") # 設定路由
def logout(): # 定義 logout 函式
    logout_user() # 登出使用者
    return redirect(url_for('home')) # 重新導向至主頁


def save_picture(form_picture): # 定義 save_picture 函式
    random_hex = secrets.token_hex(8) # 產生隨機十六進位數
    _, f_ext = os.path.splitext(form_picture.filename) # 取得檔案副檔名
    picture_fn = random_hex + f_ext # 產生檔案名稱
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # 產生檔案路徑

    output_size = (125, 125) # 設定輸出尺寸
    i = Image.open(form_picture) # 開啟圖片
    i.thumbnail(output_size) # 調整尺寸
    i.save(picture_path) # 儲存圖片

    return picture_fn # 回傳檔案名稱


@app.route("/account", methods=['GET', 'POST']) # 設定路由
@login_required # 設定登入保護
def account(): # 定義 account 函式
    form = UpdateAccountForm() # 建立 UpdateAccountForm 表單
    if form.validate_on_submit(): # 如果表單驗證成功
        if form.picture.data: # 如果有圖片
            picture_file = save_picture(form.picture.data) # 儲存圖片
            current_user.image_file = picture_file # 更新圖片
        current_user.username = form.username.data # 更新使用者名稱
        current_user.email = form.email.data # 更新電子郵件
        db.session.commit() # 提交資料庫
        flash('Your account has been updated!', 'success') # 顯示訊息
        return redirect(url_for('account')) # 重新導向至帳戶頁面
    elif request.method == 'GET': # 如果是 GET 請求
        form.username.data = current_user.username # 更新使用者名稱
        form.email.data = current_user.email # 更新電子郵件
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # 取得圖片路徑
    return render_template('account.html', title='Account', # 回傳 account.html 模板、標題、圖片路徑和表單
                           image_file=image_file, form=form)