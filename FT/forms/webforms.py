from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo

class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    role = SelectMultipleField("roles")
    submit = SubmitField("Submit")


class ImportForm(FlaskForm):
    file = FileField("file", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ProjectForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateProjectForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddApartmentForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    project = SelectField('projects')
    submit = SubmitField("Submit")

class UpdateApartmentForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    project = SelectField('projects') 
    submit = SubmitField("Submit")