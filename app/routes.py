from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/index')
@app.route('/')
@login_required
def index():
	"""主页"""
	posts = [
	        	{
	        	'author': {'username': 'LLB2'},
	        	'body': 'The first body!'
	        	}, 
	        	{'author': {'username': 'LLB3'},
	        	 'body': 'The second body!'
	        	}
	        ]
	return render_template('index.html', title='Home', posts=posts)

@app.route('/hello')
#@login_required
def hello():
	"""欢迎页（自己加的，练习用）"""
	greetingwords = {'greetingword': '欢迎'}
	return render_template('hello.html',title='Hello', greetingwords=greetingwords)

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""登陆页"""
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		###第一版###
		#flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		###第一版end###
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		#TODO: 没明白用法==========
		#print("用户随请求发送的所以信息 request.args:\n" + request.args)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		#TODOend===================
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""注册页"""
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!\n注册成功！')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form = form)

@app.route('/logout')
def logout():
	"""登出页（本函数没有登出html）"""
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	"""个人主页"""
	user = User.query.filter_by(username=username).first_or_404()
	print('User.query.filter_by(username=username):')
	print(User.query.filter_by(username=username))
	print('=============')
	print('user:')
	print(user)
	print('=============')
	posts = [
	        	{
	        	'author': user,
	        	'body': 'The first body of user1.'
	        	}, 
	        	{'author': user,
	        	 'body': 'The second body of user2.'
	        	}
	        ]
	return render_template('user.html', title='My profile', user=user, posts=posts)

@app.before_request
def before_request():
	"""
	更新user表中当前用户的last_seen项为当前时间。
	@app.before_request装饰器使被装饰函数在所有视图函数执行前执行，
	即所有视图函数执行前都会更新当前用户的last_seen
	"""
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	"""编辑个人信息页面"""
	print(current_user.about_me)
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		"""
		request.methods == 'GET'是初始请求情况，
		页面应显示当前用户原始个人信息
		"""
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

