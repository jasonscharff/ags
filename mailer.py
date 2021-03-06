import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))


#redunant, but I need to finish this.

def send_new_target(email_address, target_name, assasssin_name):
    print email_address
    from_email = Email("jason.scharff@menloschool.org", name='God')
    subject = "Your Mission"
    to_email = Email(email_address, name=assasssin_name)
    text = 'Dear {}, \n\nThe war on terror is ever evolving. While the MOAB may have gotten some of them, there is always ' \
           'more work to be done. We need you to execute {}. \n\nBe haste. \n\nGod'.format(assasssin_name, target_name)

    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    #if this doesn't send, we are kind of screwed. Maybe they'll ask?
    r = sg.client.mail.send.post(request_body=mail.get())
    print r.status_code


def send_post_kill(email_address, target_name, assasssin_name):
    from_email = Email("jason.scharff@menloschool.org", name='God')
    subject = "Your New Mission"
    to_email = Email(email_address, name=assasssin_name)
    text = 'Dear {}, \n\nYou\'ve made the world a safer place. Menlo School thanks your for your service. ' \
           'However, the bad guys keep coming. We need you to execute {}. \n\nGod'.format(assasssin_name, target_name)

    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    #if this doesn't send, we are kind of screwed. Maybe they'll ask?
    sg.client.mail.send.post(request_body=mail.get())


def send_auto_kill(email_address, assasssin_name):
    from_email = Email("jason.scharff@menloschool.org", name='God')
    subject = "You've died"
    to_email = Email(email_address, name=assasssin_name)
    text = 'Dear {}, \n\nDue to a period of inactivity, you have been retired as an asset. We wish you well in your future endeavours. \n\nGod'.format(assasssin_name)

    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    #if this doesn't send, we are kind of screwed. Maybe they'll ask?
    sg.client.mail.send.post(request_body=mail.get())