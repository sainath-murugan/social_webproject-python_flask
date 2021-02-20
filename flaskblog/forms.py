from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField



class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
             raise ValidationError("This username is already taken please try new  username")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
             raise ValidationError("This email is already taken please try new email id")

class LoginForm(FlaskForm):
   
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

class UpdateAccount(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    picture = FileField(validators=[FileAllowed(["jpg", "png"])])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError("This username is already registed please try new username name")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("This username is already registed please try new username name")


class PostForm(FlaskForm):

    content = TextAreaField("write something", validators=[DataRequired()])
    post_image = FileField(validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Post")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("there is no account with is email please register first")

class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset password") 