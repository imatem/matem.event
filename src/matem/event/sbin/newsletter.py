# -*- coding: utf-8 -*-
"""Script to be call as a cron job.

bin/instance run -O PloneSite src/x.y/x/y/testscript.py
"""
from lxml import etree
from lxml import html
from plone import api
from smtplib import SMTPRecipientsRefused


def main(app):
    portal = api.portal.get()
    view = portal.unrestrictedTraverse("acerca-de/semanaryview")
    html_view = view()
    tree = html.fragment_fromstring(html_view, create_parent=True)
    content_core = tree.xpath("//div[@id='content-core']")[0]
    mail_text = etree.tostring(content_core, pretty_print=False, encoding='utf-8')
    try:
        api.portal.send_email(
            recipient="gil@matem.unam.mx, gil@im.unam.mx",
            sender="noreply@im.unam.mx",
            subject="SEMANARIO IMUNAM",
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
