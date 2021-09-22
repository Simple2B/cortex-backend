from flask import Blueprint, request, redirect
from flask.helpers import url_for
from flask_mail import Message
from threading import Thread

from admin.config import BaseConfig as conf


from admin import mail

from app.logger import log


message_blueprint = Blueprint("message", __name__, url_prefix="/admin")


def send_async_email(msg):
    from admin.run import app

    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()


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
def index():
    data = request.form
    email = data["email"]
    text_body = "Please confirm your mail!"
    html_body = ""
    send_email(
        subject="hi",
        sender=conf.MAIL_DEFAULT_SENDER,
        recipients=email,
        text_body=text_body,
        html_body=html_body,
    )
    log(log.INFO, "MAIL_MESSAGE: mail send successfully: [%s]", send_email)
    return redirect(url_for("doctor.index_view", next=request.url))
