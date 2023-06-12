from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField, SelectMultipleField, BooleanField, SelectField, TextAreaField
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
    submit_apartment = SubmitField("Submit")

class AddApartmentNoProjectForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateApartmentForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    project = SelectField('projects')
    apartmenttype = SelectField('apartmenttype') 
    submit = SubmitField("Submit")

class UpdateApartmentNoProjectForm(FlaskForm):
    apartment_id = StringField('apartment_id', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateApartmentNoApartmenttypeForm(FlaskForm):
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

class AddApartmentTypeForm(FlaskForm):
    apartmenttype_name = StringField('apartmenttype_name', validators=[DataRequired()])
    project = SelectField('projects')
    set_standard = BooleanField("set_standard")
    submit = SubmitField("Submit")

class UpdateApartmentTypeForm(FlaskForm):
    apartmenttype_name = StringField('apartmenttype_name', validators=[DataRequired()])
    project = SelectField('projects')
    set_standard = BooleanField("set_standard")
    submit2 = SubmitField("Submit")

class AddApartmentTypeNoProjectForm(FlaskForm):
    apartmenttype_name = StringField('apartmenttype_name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class RemoveApartmentTypeForm(FlaskForm):
    apartmenttype_name = StringField('apartmenttype_name', validators=[DataRequired()])
    project = SelectField('projects')
    submit3 = SubmitField("Submit")

class AddRoomForm(FlaskForm):
    room_name = StringField('room_name', validators=[DataRequired()])
    file_upload = BooleanField("file_upload")
    submit_room = SubmitField("Submit")

class AddCategory(FlaskForm):
    category_name = StringField('category_name', validators=[DataRequired()])
    submit_category = SubmitField("Submit")

class AddToCollection(FlaskForm):
    product_id = StringField("product_id")
    project_id = StringField("project_id")
    submit2 = SubmitField("Add To Collection")

class RemoveFromCollection(FlaskForm):
    product_id = StringField("product_id")
    project_id = StringField("project_id")
    submit3 = SubmitField("Remove From Collection")

class AddCollection(FlaskForm):
    collection_name = StringField('collection_name', validators=[DataRequired()])
    project = SelectField('projects')
    submit = SubmitField("Submit")

class AddCollectionNoProjectForm(FlaskForm):
    collection_name = StringField('collection_name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateCollectionForm(FlaskForm):
    collection_name = StringField('collection_name', validators=[DataRequired()])
    project = SelectField('projects')
    submit = SubmitField("Submit")

class AddToCollection(FlaskForm):
    product_id = StringField("product_id")
    project_id = StringField("project_id")
    submit2 = SubmitField("Add To Collection")

class RemoveFromCollection(FlaskForm):
    product_id = StringField("product_id")
    project_id = StringField("project_id")
    submit3 = SubmitField("Remove From Collection")

class AddOrder(FlaskForm):
    submitOrder = SubmitField("Add order")

class DeleteOrder(FlaskForm):
    order_id = StringField("order_id")
    submitDeleteOrder = SubmitField("Delete order")

class AddToCart(FlaskForm):
    submitToCart = SubmitField("Add to cart")

class DeleteFromCart(FlaskForm):
    product_id = StringField("product_id")
    deleteFromCart = SubmitField("Delete from cart")

class AddApartmentDataToCategory(FlaskForm):
    ApartmentData = SelectField('apartmentdata')
    submitData = SubmitField("Add data")

class FileUpload(FlaskForm):
    file = FileField("file", validators=[DataRequired()])
    fileSubmit = SubmitField("Submit")