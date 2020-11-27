import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

from django.conf import settings

from ideasport_app.models import Log


def send_mail(request, match):
    mail_content = '{}. Nowy wynik w lidze IdeaSport wpisany przez: {}. {} - {}: {}'.format(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), request.user.username, match.player1_fullname(), match.player2_fullname(), match.print_result())
    Log.objects.create(message=mail_content)
    try:
        sender_address = settings.MAIL_SENDER
        sender_pass = settings.MAIL_PASSWORD
        receiver_address = [settings.MAIL1_ADDRESS, settings.MAIL2_ADDRESS]
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = (", ").join(receiver_address)
        message['Subject'] = 'Nowy wynik w lidze IdeaSport'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    except Exception:
        pass
