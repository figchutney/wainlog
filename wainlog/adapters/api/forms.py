from flask import g
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from ..postgres import persister


class Login(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    submit = SubmitField("Go!")


class Register(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    password_repeat = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Go!")

    def validate_username(self, username: StringField) -> None:
        if (
            persister.get_user_db_from_username(
                session=g.session, username=username.data
            )
            is not None
        ):
            raise ValidationError("That username is unavailable :'(")

    def validate_email(self, email: StringField) -> None:
        if (
            persister.get_user_db_from_email(
                session=g.session, email=email.data
            )
            is not None
        ):
            raise ValidationError(
                "An account with that email address already exists"
            )


class AddSummitEvent(FlaskForm):
    fell_name = HiddenField("Fell Name", validators=[DataRequired()])
    date = DateField("Summit Date", validators=[DataRequired()])
    submit = SubmitField("Climb!")


class DeleteSummitEvent(FlaskForm):
    fell_name = HiddenField("Fell Name", validators=[DataRequired()])
    submit = SubmitField("Un-climb!")
