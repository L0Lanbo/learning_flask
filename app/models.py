from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
	"""
	user表
	id 主键
	username VARCHAR(64)
	email VARCHAR(120)
	password_hash VARCHAR(128)
	about_me VARCHAR(140)
	last_seen DATE
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)#DateTime.UtcNow获取的是世界标准时区的当前时间

	def __repr__(self):
		"""用于在调试时打印用户实例"""
		return '<Use {}>'.format(self.username)

	def set_password(self, password):
		"""设置密码的方法，在数据库中存哈希值"""
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		"""核对密码"""
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		"""自动生成头像的方法（使用gravatar.loli.net国内加速）"""
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://gravatar.loli.net/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
	"""
	post表表示用户发表的动态
	id 主键
	body 具体内容字段
	timestamp 时间戳字段
	user_id 外键，关联sser表的id字段
	"""
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
	'''使用装饰器将login实例的_user_callback属性赋值为本函数，教程中称为“用户加载功能注册函数。”。'''
	return User.query.get(int(id))

