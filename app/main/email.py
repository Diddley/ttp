from flask import render_template, current_app
from app.email import send_email


def notification_email(user, cohname, state):
    send_email('System notification',
               sender=current_app.config['ADMINS'][0],
               recipients=current_app.config['OP_ADMIN'],
               text_body=render_template(
                   'email/notify.txt', user=user, state=state, cohname=cohname),
               html_body=render_template(
                   'email/notify.html', user=user, state=state, cohname=cohname))
