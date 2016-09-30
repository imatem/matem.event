# -*- coding: utf-8 -*-
"""Script to be call as a cron job.

bin/instance run -O PloneSite src/x.y/x/y/testscript.py
"""
from plone import api
from smtplib import SMTPRecipientsRefused


def main(app):

    mail_text = "http://localhost/people/9947603276956765"

    try:
        api.portal.send_email(
            recipient="informatica.academica@matem.unam.mx",
            sender="semanario@im.unam.mx",
            subject="SEMANARIO IMUNAM, 30 NOVIEMBRE - 04 DICIEMBRE, 2015",
            body=mail_text,
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
