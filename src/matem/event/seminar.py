# -*- coding: utf-8 -*-
from five import grok
from matem.event import _
from Products.CMFCore.utils import getToolByName
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IVocabularyFactory


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start time must be before the end time")


class RequiredOrganizer(Invalid):
    __doc__ = _(u"At least an organizer")


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
            default=u'Select the day, when this seminar happens.'
        ),
        vocabulary="matem.event.Weekdays"
    )

    start = schema.TextLine(
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
        # title=_(u"End date"),
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
            default=u'Organizer(s)',
        ),
        value_type=schema.Choice(
            vocabulary="matem.event.PersonVocabulary",
        ),
        required=False,
    )

    image = NamedBlobImage(
        title = _('label_seminar_image', 'Cartel'),
        required=False,
    )

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

    # TODO: Add the details field for english

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start time must be before the end time"))

    # @invariant
    # def requiredOrganizer(data):
    #     if len(data.organizer) < 1:
    #         raise RequiredOrganizer(_(u"At least an organizer"))


class View(grok.View):
    grok.context(ISeminar)
    grok.require('zope2.View')

    def getOrganizers(self):
        organizers = self.context.organizer

        catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog.searchResults(portal_type='FSDPerson', UID=organizers, sort_on='sortable_title')

        rows = []
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

        if self.context.id == 'matematicas-y-literatura':
            rows.append({'name': 'Fías Villegas Gabriela', 'url':''})

        return rows

    def getPeriodicityTitle(self):
        value = self.context.periodicity
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.PeriodicitySeminar')(self.context).by_value
        return vocabulary[value].title

    def getDayTitle(self):
        value = self.context.day
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Weekdays')(self.context).by_value
        return vocabulary[value].title
