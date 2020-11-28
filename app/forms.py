from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
	"""
	用户登陆form
	"""
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	"""
	用户注册form
	"""
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		"""
		validate_ <field_name>模式的自定应验证器，
		在已设置验证器之后调用。
		本方法在已设置的验证之后，验证用户输入数据与数据库中数据不重复。
		"""
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use different username.用户名已被使用。')

	def validate_email(self, email):
		"""
		validate_ <field_name>模式的自定应验证器，
		在已设置验证器之后调用。
		本方法在已设置的验证之后，验证用户输入数据与数据库中数据不重复。
		"""
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use different email address.电子邮箱地址已被使用。')

class EditProfileForm(FlaskForm):
	"""
	编辑个人信息的form
	"""
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About_me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')

	def __init__(self, original_name, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.original_name = original_name

	def validate_username(self, username):
		if username.data != self.original_name:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError('Please use different username.用户名已被使用。')

		
