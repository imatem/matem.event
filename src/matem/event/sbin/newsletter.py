# -*- coding: utf-8 -*-
"""Script to be call as a cron job.

bin/client -O PloneSite run src/x.y/x/y/testscript.py
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import etree
from lxml import html
from plone import api
from premailer import transform
from smtplib import SMTPRecipientsRefused


def main(app):
    portal = api.portal.get()
    view = portal.unrestrictedTraverse("acerca-de/semanaryview")
    html_view = view()

    # apply inline style
    pmail = transform(html_view)
    tree = html.fragment_fromstring(pmail, create_parent=True)
    content_core = tree.xpath("//div[@id='content-core']")[0]

    # Create the body of the message (a plain-text and an HTML version).
    html_text = etree.tostring(content_core, pretty_print=False, encoding='utf-8')
    html_text = html_text.replace('nohost/infomatem', 'www.matem.unam.mx')

    transforms = api.portal.get_tool('portal_transforms')
    stream = transforms.convertTo('text/plain', html_text, mimetype='text/html')
    text = stream.getData().strip()

    # Create message container - the correct MIME type is multipart/alternative.
    message = MIMEMultipart('alternative')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    message.attach(MIMEText(text, 'plain'))
    message.attach(MIMEText(html_text, 'html'))
    try:
        api.portal.send_email(
            recipient="gil@matem.unam.mx",
            sender="difusion@im.unam.mx",
            subject="SEMANARIO IMUNAM",
            body=message,
            immediate=True,
        )
    except SMTPRecipientsRefused:
        # Don't disclose email address on failure
        raise SMTPRecipientsRefused('Recipient address rejected by server')


# If this script lives in your source tree, then we need to use this trick so that
# five.grok, which scans all modules, does not try to execute the script while
# modules are being loaded on the start-up
if "app" in locals():
    main(app)

# (Pdb++) from premailer import Premailer
# (Pdb++) import logging
# (Pdb++) pmail = Premailer(html_view, cssutils_logging_level=logging.CRITICAL)
# (Pdb++) result = pmail.transform()
