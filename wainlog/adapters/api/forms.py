from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired


class AddSummitEvent(FlaskForm):
    fell_name = HiddenField("Fell Name", validators=[DataRequired()])
    date = DateField("Summit Date", validators=[DataRequired()])
    submit = SubmitField("Climb!")


class DeleteSummitEvent(FlaskForm):
    fell_name = HiddenField("Fell Name", validators=[DataRequired()])
    submit = SubmitField("Un-climb!")
