# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.app.appsetup.product
import zope.component
import zope.sendmail.delivery
import zope.sendmail.interfaces
import zope.sendmail.mailer
import zope.sendmail.queue

import email.encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


COMMASPACE = ', '


config = zope.app.appsetup.product.getProductConfiguration('mailer')
if config is not None:
    queue_path = config.get('queue-path')
    hostname = config.get('hostname', 'localhost')
    port = int(config.get('port', 25))
    # treat username and password as non-existent if they're empty strings
    username = config.get('username', None) or None
    password = config.get('password', None) or None


    mailer_object = zope.sendmail.mailer.SMTPMailer(
        hostname, port, username, password, force_tls=False)

    def mailer():
        return mailer_object

    def delivery():
        return zope.sendmail.delivery.QueuedMailDelivery(queue_path)

    def start_processor_thread():
        thread = zope.sendmail.queue.QueueProcessorThread()
        thread.setMailer(mailer_object)
        thread.setQueuePath(queue_path)
        thread.start()
    grok.global_utility(
        mailer,
        provides=zope.sendmail.interfaces.IMailer,
        name='uvcsite.smtpmailer')

    grok.global_utility(
        delivery,
        zope.sendmail.interfaces.IMailDelivery,
        name='uvcsite.maildelivery')

    start_processor_thread()


def get_mailer():
    return zope.component.getUtility(
        zope.sendmail.interfaces.IMailDelivery,
        name=u'uvcsite.maildelivery'
    )


def send_mail(sender, recipient, subject, body, file=None, filename=None):
    '''
    Funktion zum versenden von Emails
    recipient muss als Liste übergeben werden
    body sollte einen formatierter String sein
    '''

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = COMMASPACE.join(recipient)  # List to String
    msg["Subject"] = email.header.Header(subject, 'UTF-8')
    msg.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))

    # Attachment von Dateien
    if file is not None:
        fn = file.split("/")
        fn = fn[-1]
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        email.encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename=%s' % filename or fn
            )
        msg.attach(part)
    mailer = get_mailer()
    mailer.send(sender, recipient, msg.as_string())
