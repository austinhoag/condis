from flask import Markup
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
					 BooleanField, HiddenField, IntegerField, FieldList, FormField,
					 SelectMultipleField,DecimalField)
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 
from wtforms.widgets import html5, CheckboxInput, ListWidget
# from wtforms.fields.html5 import DateTimeLocalField

datetimeformat='%Y-%m-%dT%H:%M' # To get form.field.data to work. Does not work with the default (bug)

# from lightserv.models import Experiment

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
	