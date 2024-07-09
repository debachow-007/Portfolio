from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, TextAreaField, SubmitField # type: ignore
from wtforms.validators import DataRequired, Email # type: ignore

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
