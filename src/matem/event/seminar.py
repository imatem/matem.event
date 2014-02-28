# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from matem.event import _
from five import grok
from plone.app.textfield import RichText
#from plone.directives import form
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

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unicodedata




class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start date must be before the end date")


class RequiredOrganizer(Invalid):
    __doc__ = _(u"At least organizer")


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
        vocabulary="matem.event.Weekdays"
    )

    start = schema.TextLine(
        #title=_(u"Start time"),
        title=_(
            u'label_seminar_start',
            default=u'Start time'
        ),
        description=_(
            u'help_seminar_start',
            default=u'Type the start time, when this seminar happens. The time format is hh:mm.'
        ),
        required=False,
        max_length=5,
    )

    end = schema.TextLine(
        #title=_(u"End date"),
        title=_(
            u'label_seminar_end',
            default=u'End time'
        ),
        description=_(
            u'help_seminar_end',
            default=u'Type the end time, when this seminar happens. The time format is hh:mm.'
        ),
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

    periodicity = schema.Choice(
        title=_(
            u'label_seminar_periodicity',
            default=u'Periodicity'
        ),
        description=_(
            u'help_seminar_periodicity',
            default=u'Periodicity of the seminar.'
        ),
        required=False,
        vocabulary="matem.event.PeriodicitySeminar"

    )

    organizer = schema.List(
        title=_(
            u'label_seminar_organizer',
            default=u'Organizer',
        ),
        value_type=schema.Choice(
            vocabulary="matem.event.PersonVocabulary",
        ),
        required=True,
        #default=set([1,3])
    )

    # details = RichText(
    #     title=_(u"Details"),
    #     description=_(u"Details about the seminar"),
    #     default_mime_type='text/structured',
    #     output_mime_type='text/html',
    #     allowed_mime_types=('text/structured', 'text/plain',),
    #     required=False,
    
    # )

    form.widget('details', WysiwygFieldWidget)
    details = schema.Text(
        title=_(
            u'label_seminar_details', 
            default=u'Details'
        ),
        description=_(
            u'help_seminar_details',
            u'Details about the seminar'
        ),
        required=False,
    )



    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date"))

    @invariant
    def requiredOrganizer(data):
        if len(data.organizer) < 1:
            raise RequiredOrganizer(_(u"At least an organizer"))
        
# Views
class View(grok.View):
    grok.context(ISeminar)
    grok.require('zope2.View')

    def getOrganizers(self):
        organizers = self.context.organizer

        catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog.searchResults(portal_type='FSDPerson', UID=organizers)

        rows =[]
        for b in brains:
            obj = b.getObject()
            rows.append(
                {
                    'url': obj.absolute_url(),
                    'name': ', '.join((b.lastName, b.firstName)),
                    'phone': obj.getOfficePhone(),
                    'email': obj.getEmail(),
                }
            )

        return rows

    def getPeriodicityTitle(self):
        value = self.context.periodicity
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.PeriodicitySeminar')(self.context).by_value
        return vocabulary[value].title

    def getDayTitle(self):
        value = self.context.day
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Weekdays')(self.context).by_value
        return vocabulary[value].title



