from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from wtforms.fields.html5 import DateTimeField
from datetime import datetime

'''Form for task creation and updation'''
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Description', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"},validators=[DataRequired()])
    end_time = DateTimeField('End Time', render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"},validators=[DataRequired()])
    submit = SubmitField('Submit')