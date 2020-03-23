from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from exts import db, login_manager
from models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from forms import LoginForm, SignupForm, WriteForm, EditForm
import mistune
from markupsafe import Markup
from post import postbp


app = Flask(__name__)

# blueprint register
app.register_blueprint(postbp, url_prefix='/post')

# config of flask app
app.config.from_object('config')
#      
db.init_app(app)
login_manager.init_app(app)

# routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None and (form.password.data == form.password_again.data):
            password_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('signin'))
        else:
            flash('user is registered')
    if form.errors:
        flash('failed to log in', 'danger')
    return render_template('signup.html', form=form)

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    fmtpost = []
    for post in posts:
        temp = {
            'id':post.id,
            'title':post.title,
            'time': post.create_time.strftime("%b %d, %Y")
        }
        fmtpost.append(temp)
    return render_template('home.html', posts=fmtpost)

@app.route('/signin',methods=['GET','POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('password is wrong')
            return redirect(url_for('signup'))
    if form.errors:
        flash('failed to log in', 'danger')
    return render_template('signin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/admin/')
@login_required
def manage():
    posts = Post.query.all()
    fmtpost = []
    for post in posts:
        temp = {
            'id':post.id,
            'title':post.title,
            'time': post.create_time.strftime("%b %d, %Y")
        }
        fmtpost.append(temp)
    return render_template('manage.html', posts=fmtpost)


@app.route('/about')
def about():
    return render_template('about.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.route('/sitemap.xml')
def sitemap():
    posts = Post.query.all()
    fmtpost = []
    for post in posts:
        temp = {
            'id':post.id,
            'time': post.create_time.strftime("%Y-%m-%d")
        }
        fmtpost.append(temp)
    template = render_template('sitemap/sitemap.xml', posts=fmtpost)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/yandex_3eeaa5d2b933e925.html')
def yandex():
    return render_template('yandex/yandex_3eeaa5d2b933e925.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')