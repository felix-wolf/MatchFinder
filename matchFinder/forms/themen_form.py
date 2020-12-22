from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class ThemaEntryForm(FlaskForm):
	thema_name = StringField('Name', validators=[DataRequired()])
	zeit = StringField('Zeitpunkt')
	betreuer = StringField('Betreuer')


class ThemenForm(FlaskForm):
	themen_name = StringField('Name', validators=[DataRequired()])
	themen = FieldList(FormField(ThemaEntryForm), validators=[DataRequired()])
