from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    roll_no = StringField('Roll No', validators=[DataRequired(), Length(max=150)])
    branch = StringField('Branch', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('Register')
