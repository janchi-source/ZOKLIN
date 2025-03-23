from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, BooleanField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Account Type', choices=[('customer', 'Customer'), ('provider', 'Service Provider')])
    
    # Provider-specific fields (optional for customers)
    company_name = StringField('Company Name', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Company Description', validators=[Optional()])
    services = StringField('Services Offered (comma-separated)', validators=[Optional()])
    location = SelectField('Location', 
                         choices=[('bratislava', 'Bratislava'), ('pezinok', 'Pezinok')],
                         validators=[Optional()])
    price_from = FloatField('Starting Price (€)', validators=[Optional()])
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    service_type = SelectField('Service Type', choices=[
        ('house', 'House Cleaning'),
        ('office', 'Office Cleaning'),
        ('garden', 'Garden Services'),
        ('car', 'Car Cleaning'),
        ('mental', 'Mental Cleaning')
    ], validators=[DataRequired()])
    booking_date = StringField('Preferred Date and Time', validators=[DataRequired()])
    notes = TextAreaField('Special Requirements or Notes')
    submit = SubmitField('Book Now')

class ProviderProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Company Description', validators=[DataRequired()])
    services = StringField('Services Offered (comma-separated)', validators=[DataRequired()])
    location = SelectField('Location', 
                         choices=[('bratislava', 'Bratislava'), ('pezinok', 'Pezinok')],
                         validators=[DataRequired()])
    price_from = FloatField('Starting Price (€)', validators=[DataRequired()])
    availability = StringField('Availability (JSON format)', validators=[Optional()])
    submit = SubmitField('Update Profile')

class ServiceOfferForm(FlaskForm):
    service_type = SelectField('Service Type', choices=[
        ('house', 'House Cleaning'),
        ('office', 'Office Cleaning'),
        ('garden', 'Garden Services'),
        ('car', 'Car Cleaning'),
        ('mental', 'Mental Cleaning')
    ], validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (€)', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[Optional()])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Offer')