from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from matem.event import _
from five import grok
from plone.app.textfield import RichText
from plone.directives import form
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.indexer import indexer
from plone.supermodel import model
from z3c.form.browser.textlines import TextLinesFieldWidget
from zope import schema
from zope.component import createObject
from zope.event import notify
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import invariant, Invalid
from zope.lifecycleevent import ObjectCreatedEvent
import datetime


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class ISeminar(model.Schema):
    """A folder for Seminars.
    """

    day = schema.Choice(
        title=_(
            u'label_seminar_day',
            default=u'Day'
        ),
        description=_(
            u'help_seminar_day',
            default=u'Select the day, where this seminar happens.'
        ),
        required=True,
        vocabulary="plone.app.event.Weekdays"
    )


    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
    )

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
    )

    location = schema.TextLine(
        title=_(
            u'label_seminar_location',
            default=u'Location'
        ),
        description=_(
            u'help_seminar_location',
            default=u'Location of the seminar.'
        ),
        required=False
    )

    organizer = schema.Choice(
        title=_(u"Organizer"),
        vocabulary=u"plone.app.event.Weekdays",
        required=False,
    )

    details = RichText(
        title=_(u"Details"),
        description=_(u"Details about the seminar"),
        default_mime_type='text/structured',
        output_mime_type='text/html',
        allowed_mime_types=('text/structured', 'text/plain',),
        required=False,
    )


    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))

# Views
class View(grok.View):
    grok.context(ISeminar)
    grok.require('zope2.View')


