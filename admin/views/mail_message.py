from urllib.parse import urljoin
from flask import Blueprint, request, redirect, render_template
from flask.helpers import url_for
from flask_mail import Message

from admin.config import BaseConfig as conf
from admin import mail
from admin.forms import NewDoctorForm
from app.models import Doctor

from app.logger import log


message_blueprint = Blueprint("message", __name__, url_prefix="/admin")


def send_email(subject, sender, recipients: list[str], text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


# def send_mail_to_user_without_passwd():
#     doctors = Doctor.query.all()
#     for doctor in doctors:
#         if doctor.hash_password == None:
#             email = doctor.email
#             text_body = "Please confirm your mail!"
#             html_body = ""
#             send_email(
#                 subject="hi",
#                 sender=conf.MAIL_DEFAULT_SENDER,
#                 recipients=[email],
#                 text_body=text_body,
#                 html_body=html_body,
#             )
#             log(log.INFO, "MAIL_MESSAGE: mail send successfully: [%s]", send_email)
#             return redirect(url_for("doctor.index_view"))
#         log(log.ERROR, "MAIL_MESSAGE: mail didn't send: [%s]", send_email)
#         return redirect(url_for("doctor.index_view"))


# @message_blueprint.route("/doctor/")
# def index():
#     send_mail_to_user_without_passwd()


@message_blueprint.route("/doctor/new/", methods=["POST"])
def new_doctor():
    form = NewDoctorForm()
    if form.validate_on_submit():
        email = form.email.data
        doc = Doctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            role=Doctor.DoctorRole(form.role.data),
        ).save()
        link = urljoin(
            request.host_url, conf.URL_REG_DOCTOR.format(api_key=doc.api_key)
        )
        text_body = link
        html_body = render_template(
            "register_email.html",
            doctor=doc,
            link=link,
        )
        send_email(
            subject=f"{conf.APP_NAME} registration",
            sender=conf.MAIL_DEFAULT_SENDER,
            recipients=[
                email,
            ],
            text_body=text_body,
            html_body=html_body,
        )
        log(log.INFO, "MAIL_MESSAGE: mail send successfully: [%s]", send_email)
        return redirect(url_for("doctor.index_view", next=request.url))
    else:
        return redirect(url_for("doctor.create_view", next=request.url))
