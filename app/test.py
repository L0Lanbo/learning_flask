from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
	"""
	使用unittest包进行单元测试
	20201212：测试四个用户模型的测试，包含密码哈希、用户头像和粉丝功能
	"""
	def setUp(self):
		"""测试工程执行前执行的特殊方法"""
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(sefl):
		"""测试工程执行后执行的特殊方法"""
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		'''User的setpassword()和check_password()方法'''
		u = User(username='susan')
		u.set_password('cat')
		self.asserFalse(u.check_password('ca'))
		self.asserTrue(u.check_password('cat'))

	





