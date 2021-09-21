from flask import Blueprint, request, redirect, render_template
from flask.helpers import url_for
from flask_mail import Message
from threading import Thread

from admin.config import BaseConfig as conf

from admin import mail
from app.logger import log


message_blueprint = Blueprint("message", __name__, url_prefix="/admin")


def send_async_email(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()


@message_blueprint.route("/doctor/new/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_body = "Please confirm your mail!"
        html_body = ""
        send_email(
            subject="hi",
            sender=conf.MAIL_SENDER,
            recipients=[request.form.get("Email")],
            text_body=text_body,
            html_body=html_body,
        )
        log(log.INFO, "MAIL_MESSAGE: mail send successfully: [%s]", send_email)
        return redirect(url_for("doctor.index_view"))
    else:
        log(log.ERROR, "MAIL_MESSAGE: mail didn't send: [%s]", send_email)
        return render_template("<div> Confirmation not sent by mail </div>")
