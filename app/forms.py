from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import Required, DataRequired, Length
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[
                           Required(), DataRequired(), Length(max=16)])
    password1 = PasswordField("password1", validators=[
                              Required(), DataRequired()])
    password2 = PasswordField("password2", validators=[Required()])


class LoginForm(FlaskForm):
    username = StringField("username", validators=[
                           Required(), DataRequired(), Length(max=16)])
    password = PasswordField("password", validators=[
                             Required(), DataRequired()])


class AddArticleForm(FlaskForm):
    username = HiddenField("username", validators=[Required(), DataRequired()])
    title = StringField("title", validators=[
                        Required(), DataRequired(), Length(max=100)])
    text = TextAreaField("text", validators=[Required(), DataRequired()])
    intro = StringField("intro", validators=[
                        Required(), DataRequired(), Length(max=100)])


class AddCommentForm(FlaskForm):
    commentText = StringField("commentText", validators=[
                              Required(), DataRequired(), Length(max=300)])
    articleID = HiddenField("articleID", validators=[
                            Required(), DataRequired()])
    userID = HiddenField("userID", validators=[Required(), DataRequired()])
