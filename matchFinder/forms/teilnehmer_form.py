from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class TeilnehmerEntryForm(FlaskForm):
	first_name = StringField('Vorname', validators=[DataRequired()])
	last_name = StringField('Nachname')
	matr_nr = IntegerField('Matrikelnummer')


class TeilnehmerForm(FlaskForm):
	teilnehmer_name = StringField('Name', validators=[DataRequired()])
	teilnehmer = FieldList(FormField(TeilnehmerEntryForm), validators=[DataRequired()])
