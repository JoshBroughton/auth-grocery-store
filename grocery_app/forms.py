from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore

def store_factory():
    return GroceryStore.query.all()

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Title', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    address = StringField('Address', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
    name = StringField('Name', validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your message needs to be betweeen 3 and 80 chars")
        ])
    price = FloatField('Price', validators=[DataRequired()])
    cateogry = SelectField('Category',
        validators=[DataRequired()],
        chocies=[
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
    store = QuerySelectField('Store', query_factor=store_factory, validators=[DataRequired()])
    submit = SubmitField('Submit')
