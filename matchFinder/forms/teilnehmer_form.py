from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class TeilnehmerEntryForm(FlaskForm):
	"""
	defines a WTForm for the a single teilnehmer with 3 fields.
	first_name and matr_nr are required while last_name is optional.
	"""
	first_name = StringField('Vorname', validators=[DataRequired()])
	last_name = StringField('Nachname')
	matr_nr = IntegerField('Matrikelnummer', validators=[DataRequired()])


class TeilnehmerForm(FlaskForm):
	"""
	this class defines a WTForm for a list of teilnehmer.
	It does so by asking for a name and a list of teilnehmerEntries,
	which are defined above.
	Both the name and the list are required.
	"""
	teilnehmer_name = StringField('Name', validators=[DataRequired()])
	teilnehmer = FieldList(FormField(TeilnehmerEntryForm),
		validators=[DataRequired()])
