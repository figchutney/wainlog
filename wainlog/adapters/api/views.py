from flask import Blueprint, flash, g, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug import Response

from ...core import types
from ..postgres import model, persister
from . import forms, view_functions

bp = Blueprint(name="wainlog", import_name=__name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def root() -> str | Response:
    fells_by_book = view_functions.get_fells_by_book(session=g.session)
    summit_events: list[types.SummitEvent] | None = None

    if current_user.is_authenticated:
        add_summit_form = forms.AddSummitEvent()
        delete_summit_form = forms.DeleteSummitEvent()

        if add_summit_form.validate_on_submit():
            persister.add_summit_event(
                session=g.session,
                user_id=current_user.get_id(),
                fell_name=types.FellName(add_summit_form.fell_name.data),
                summit_date=add_summit_form.date.data,
            )
            g.session.commit()
            summit_events = persister.get_summit_events_for_user(
                session=g.session, username=current_user.username
            )
            return redirect(url_for("wainlog.root"))
        elif delete_summit_form.validate_on_submit():
            persister.delete_summit_event(
                session=g.session,
                user_id=current_user.get_id(),
                fell_name=types.FellName(delete_summit_form.fell_name.data),
            )
            g.session.commit()
            summit_events = persister.get_summit_events_for_user(
                session=g.session, username=current_user.username
            )
            return redirect(url_for("wainlog.root"))

        summit_events = persister.get_summit_events_for_user(
            session=g.session, username=current_user.username
        )
        return render_template(
            "root.html",
            fells_by_book=fells_by_book,
            summit_events=summit_events,
            add_summit_form=add_summit_form,
            delete_summit_form=delete_summit_form,
        )

    return render_template(
        "root.html",
        fells_by_book=fells_by_book,
        summit_events=summit_events,
    )


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("wainlog.root"))

    form = forms.Login()

    if form.validate_on_submit():
        user = persister.get_user_db_from_username(
            session=g.session, username=form.username.data
        )

        if user is None or user.check_password(form.password.data) is False:
            flash("Invalid username or password")
            return redirect(url_for("wainlog.login"))
        login_user(user)

        return redirect(url_for("wainlog.root"))

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    logout_user()

    return redirect(url_for("wainlog.root"))


@bp.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("root"))

    form = forms.Register()

    if form.validate_on_submit():
        user = model.User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        persister.add_user(session=g.session, user=user)
        g.session.commit()
        return redirect(url_for("wainlog.login"))

    return render_template("register.html", title="Register", form=form)
