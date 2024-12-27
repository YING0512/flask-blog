import os # 匯入 os 模組
import secrets # 匯入 secrets 模組 
from PIL import Image # 匯入 Image 類別，用於處理圖片 
from flask import render_template, url_for, flash, redirect, request # 匯入 render_template、url_for、flash、redirect 和 request 函數，用於處理請求和返回頁面
from flaskblog import app, db, bcrypt # 匯入 app、db 和 bcrypt 實例，用於應用和資料庫操作
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # 匯入註冊、登入和更新帳戶表單類別，用於表單驗證
from flaskblog.models import User, Post # 匯入 User 和 Post 類別，用於操作使用者和文章資料
from flask_login import login_user, current_user, logout_user, login_required # 匯入登入、當前用戶、登出和登入必須的裝飾器，用於處理用戶登入


# 假資料：模擬的部落格文章列表
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


# 設置主頁路由
@app.route("/")
@app.route("/home")
def home():
    # 渲染 home.html 模板並傳遞 posts 變數
    return render_template('home.html', posts=posts)


# 設置關於頁面路由
@app.route("/about")
def about():
    # 渲染 about.html 模板並傳遞 title 變數
    return render_template('about.html', title='About')


# 註冊頁面路由，支持 GET 和 POST 請求
@app.route("/register", methods=['GET', 'POST'])
def register():
    # 如果使用者已經登入，重定向至首頁
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # 創建註冊表單實例
    form = RegistrationForm()

    # 如果表單提交並且驗證成功
    if form.validate_on_submit():
        # 加密密碼
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 創建新用戶實例並添加至資料庫
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # 註冊成功後重定向到登入頁面
        return redirect(url_for('login'))
    
    # 如果不是 POST 請求，渲染註冊頁面
    return render_template('register.html', title='Register', form=form)


# 登入頁面路由，支持 GET 和 POST 請求
@app.route("/login", methods=['GET', 'POST'])
def login():
    # 如果使用者已經登入，重定向至首頁
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # 創建登入表單實例
    form = LoginForm()

    # 如果表單提交並且驗證成功
    if form.validate_on_submit():
        # 根據電子郵件查詢用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 如果用戶存在且密碼驗證成功
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # 獲取登入後重定向的頁面（如果有）
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    # 如果不是 POST 請求，渲染登入頁面
    return render_template('login.html', title='Login', form=form)


# 登出頁面路由
@app.route("/logout")
def logout():
    # 執行登出
    logout_user()
    # 重定向至首頁
    return redirect(url_for('home'))


# 用於儲存上傳的頭像圖片
def save_picture(form_picture):
    # 生成隨機的文件名
    random_hex = secrets.token_hex(8)
    # 獲取圖片檔案的副檔名
    _, f_ext = os.path.splitext(form_picture.filename)
    # 設置儲存路徑
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # 設定圖片大小並儲存
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # 返回儲存後的檔案名
    return picture_fn


# 用戶帳戶頁面路由，要求登入
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # 創建更新帳戶表單實例
    form = UpdateAccountForm()

    # 如果表單提交並且驗證成功
    if form.validate_on_submit():
        # 如果上傳了新頭像，儲存並更新頭像檔案名
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # 更新使用者的帳戶資料
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # 更新完成後重定向回帳戶頁面
        return redirect(url_for('account'))

    # 如果是 GET 請求，預先填充表單
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # 獲取用戶的頭像圖片路徑
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 渲染帳戶頁面並傳遞圖片路徑和表單
    return render_template('account.html', title='Account', image_file=image_file, form=form)
