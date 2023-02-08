from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, FloatField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from grocery_app.models import GroceryStore, User
from grocery_app.extensions import bcrypt

def store_factory():
    return GroceryStore.query.all()

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Title', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    address = StringField('Address', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Name', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category',
        validators=[DataRequired()],
        choices=[
            ('PRODUCE','Produce'), 
            ('DELI ', 'Deli'), 
            ('BAKERY', 'Bakery'),
            ('PANTRY ', 'Pantry'),
            ('FROZEN', 'Frozen'),
            ('OTHER', 'Other')
            ]
        )
    photo_url = StringField('photo_url', validators=[
            DataRequired(), 
            Length(min=3, max=200, message="Your url needs to be betweeen 3 and 200 chars")
        ])
    store = QuerySelectField('Store', query_factory=store_factory, validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

class SignUpForm(FlaskForm):
    username = StringField('User Name',
            validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
