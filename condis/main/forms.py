from flask import Markup
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
					 BooleanField, HiddenField, IntegerField, FieldList, FormField,
					 SelectMultipleField,DecimalField)
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 
from wtforms.widgets import html5, CheckboxInput, ListWidget
from geopy.geocoders import Nominatim
# from wtforms.fields.html5 import DateTimeLocalField

datetimeformat='%Y-%m-%dT%H:%M' # To get form.field.data to work. Does not work with the default (bug)

	
class EntryForm(FlaskForm):
	""" The form for requesting a recurring email based on location """
	gps_str = StringField('Latitude,Longitude (e.g. 36.131,-115.425):',validators=[InputRequired()])
	address = StringField('''Address or Zip Code (e.g. "Red Rock Canyon, NV USA" or "89161 USA"):''',validators=[Optional()])

	temp = StringField(Markup('Temperature (&deg;F)'),id='temp-field')
	time = StringField(Markup('Time of day'),id='time-field')

	humidity = StringField('Relative Humidity (%)',id='humidity-field')
	precip = StringField('Percent chance of precipitation (%)',id='precip-field')
	email_check = BooleanField("Check to also receive an email whenever these conditions are met.")
	email = StringField('Your email:',validators=[Optional(),Email()])
	submit = SubmitField("Search")

	def validate_gps_str(self,gps_str):
		try:
			splitstr = gps_str.data.split(',')
		except:
			raise ValidationError('Incorrect format. Try again.')
		if len(splitstr) != 2:
			raise ValidationError('Incorrect format. Acceptable format is latitude,longitude')
		try:	
			lat = float(splitstr[0])
			lon = float(splitstr[1])
		except:
			raise ValidationError('Incorrect format. Try again.')

	def validate_address(self,address):
		geolocator = Nominatim(user_agent="my-app")
		location = geolocator.geocode(address.data)
		try:
			latitude, longitude = location.latitude,location.longitude
		except:
			raise ValidationError("Address not valid. Try again")

	

class gpsForm(FlaskForm):
	""" The form for requesting a new experiment/dataset """
	
	# Basic info
	latitude = DecimalField('Latitude (-90,+90):',validators=[InputRequired()])
	longitude = DecimalField('Longitude (-180,+180):',validators=[InputRequired()])
	submit = SubmitField("Submit")

	def validate_latitude(self,latitude):
		if not (-90 < latitude.data < 90):
			raise ValidationError("Latitude must be within (-90,+90)")
	def validate_longitude(self,longitude):
		if not (-180 < longitude.data < 180):
			raise ValidationError("Longitude must be within (-180,+180)")

class SetupForm(FlaskForm):
	""" The form for requesting a new experiment/dataset """

	gps_str = StringField('Latitude/Longitude (e.g. 36.131,-115.425):',validators=[InputRequired()])
	temp = StringField(Markup('Temperature (&deg;F)'),id='temp-field')
	humidity = StringField('Relative Humidity (%)',id='humidity-field')
	precip = StringField('Percent chance of precipitation (%)',id='precip-field')
	# latitude = DecimalField('Latitude (-90,+90):',validators=[InputRequired()])
	# longitude = DecimalField('Longitude (-180,+180):',validators=[InputRequired()])
	submit = SubmitField("Submit")

	def validate_gps_str(self,latitude):
		try:
			splitstr = gps_str.split(',')
			if len(splitstr) != 2:
				raise ValidationError('Incorrect format. Acceptable format is latitude,longitude')
			lat = float(splitstr[0])
			lon = float(splitstr[1])
		except:
			raise ValidationError('Incorrect format. Try again.')

class SetupRecurringForm(FlaskForm):
	""" The form for requesting a recurring email based on location """
	email = StringField('Your email:',validators=[Email(),InputRequired()])
	gps_str = StringField('Latitude,Longitude (e.g. 36.131,-115.425):',validators=[InputRequired()])
	temp = StringField(Markup('Temperature (&deg;F)'),id='temp-field')
	humidity = StringField('Relative Humidity (%)',id='humidity-field')
	precip = StringField('Percent chance of precipitation (%)',id='precip-field')
	submit = SubmitField("Submit")

	def validate_gps_str(self,gps_str):
		try:
			splitstr = gps_str.data.split(',')
		except:
			raise ValidationError('Incorrect format. Try again.')
		if len(splitstr) != 2:
			raise ValidationError('Incorrect format. Acceptable format is latitude,longitude')
		try:	
			lat = float(splitstr[0])
			lon = float(splitstr[1])
		except:
			raise ValidationError('Incorrect format. Try again.')
