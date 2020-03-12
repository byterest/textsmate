from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired()])
    password = PasswordField('密码', validators=[InputRequired()])

class SignupForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired()])
    password = PasswordField('密码', validators=[InputRequired()])
    password_again = PasswordField('再次输入密码', validators=[InputRequired()])

class WriteForm(FlaskForm):
    title = StringField('标题', validators=[InputRequired()])
    body = TextAreaField('内容',validators=[InputRequired()])

class EditForm(FlaskForm):
    title = StringField('标题', validators=[InputRequired()])
    body = TextAreaField('内容', validators=[InputRequired()])
    