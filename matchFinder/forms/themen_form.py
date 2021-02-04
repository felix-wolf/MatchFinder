from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class ThemaEntryForm(FlaskForm):
	"""
	defines a WTForm for the a single thema with 3 fields.
	thema_name is required (meaning it needs non-empty data),
	while zeit and betreuer are optional.
	"""
	thema_name = StringField('Name', validators=[DataRequired()])
	zeit = StringField('Zeitpunkt')
	betreuer = StringField('Betreuer')


class ThemenForm(FlaskForm):
	"""
	this class defines a WTForm for a list of themen.
	It does so by asking for a name and a list of themaEntries,
	which are defined above.
	Both the name and the list are required.
	"""
	themen_name = StringField('Name', validators=[DataRequired()])
	themen = FieldList(FormField(ThemaEntryForm), validators=[DataRequired()])
