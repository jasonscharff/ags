import sendgrid
import os
from sendgrid.helpers.mail import *


def send_new_target(email_address, target_name, asasssin_name):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("jason.scharff@menloschool.org", name='God')
    subject = "Assignment"
    to_email = Email(email_address, name=asasssin_name)
    content = Content("text/plain", "Hello, Email!")
    mail = Mail(from_email, subject, to_email, content)
    #if this doesn't send, we are kind of screwed. Maybe they'll ask?
    sg.client.mail.send.post(request_body=mail.get())
