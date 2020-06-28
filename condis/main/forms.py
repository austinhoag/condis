from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField)
from wtforms.fields.html5 import DecimalRangeField

class SetupForm(FlaskForm):
	age = DecimalRangeField('Age', default=0)
	
	submit = SubmitField("Submit Feedback")