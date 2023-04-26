from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, BooleanField, SelectField, TextAreaField
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
    apartment = SelectField('apartment')
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

class AddApartmentNoProjectForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateApartmentForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    project = SelectField('projects') 
    submit = SubmitField("Submit")

class AddProductForm(FlaskForm):
    nrf = StringField('nrf', validators=[DataRequired()])
    leverandor = StringField('leverandor', validators=[DataRequired()]) 
    hovedkategori = StringField('hovedkategori', validators=[DataRequired()])
    underkategori = StringField('underkategori', validators=[DataRequired()])
    kategori = StringField('kategori', validators=[DataRequired()])
    produktnavn = StringField('produktnavn', validators=[DataRequired()])
    beskrivelse = TextAreaField('beskrivelse', validators=[DataRequired()])
    mal = StringField('mal')
    farge = StringField('farge')
    enhet = StringField('enhet')
    submit = SubmitField("Submit")
class AddCollection(FlaskForm):
    collection_name = StringField('collection_name', validators=[DataRequired()])
    submit = SubmitField("Submit")