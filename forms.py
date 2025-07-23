from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    age = StringField('Age', validators=[InputRequired()])
    bio = StringField('Bio', validators=[InputRequired(), Length(max=200)])
    interests = StringField('Interests', validators=[InputRequired(), Length(max=100)])
    submit = SubmitField('Update Profile')