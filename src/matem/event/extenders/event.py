# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.interfaces import IATEvent
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from five import grok
from matem.event import _
from plone.indexer.decorator import indexer
from zope import component
from zope import interface
from zope.component.hooks import getSite
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class _StringExtensionField(ExtensionField, atapi.StringField):
    '''Any field you can tack on must have ExtensionField as its first subclass
    '''
    pass


class _LinesExtensionField(ExtensionField, atapi.LinesField):
    '''Any field you can tack on must have ExtensionField as its first subclass
    '''
    pass

BasicSchema = [

    _StringExtensionField(
        name='isIMember',
        required=True,
        vocabulary_factory='matem.event.isIMember',
        enforceVocabulary=1,
        default='no',
        widget=MasterSelectWidget(
            label=_(u'Is the speaker IM Researcher Member?'),
            description=_(u'Select Yes if the speaker is a Researcher of IM. Remember that Speaker name is required.'),
            i18n_domain='matem.event',
            slave_fields=(
                {'name': 'internal_speaker', 'action': 'hide', 'hide_values': ('no',)},
                {'name': 'institution', 'action': 'hide', 'hide_values': ('yes',)},
                {'name': 'speaker', 'action': 'hide', 'hide_values': ('yes',)},
            ),
        ),
    ),

    _StringExtensionField(
        name='internal_speaker',
        vocabulary_factory='matem.event.speakersVocabulary',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Speaker name'),
            description=_(u'Select the speaker name'),
            i18n_domain='matem.event',
            size=60,
        ),
        validators=('isEmptyInternalSpeakerValidator', ),
    ),

    _StringExtensionField(
        name='speaker',
        widget=atapi.StringWidget(
            label=_(u'Speaker name'),
            description=_(u'Type the Speaker Name'),
            i18n_domain='matem.event',
            size=60,
        ),
        validators=('isEmptyExternalSpeakerValidator', ),
    ),

    _StringExtensionField(
        name='institution',
        widget=atapi.StringWidget(
            label=_(u'Institution'),
            i18n_domain='matem.event',
            size=60,
        ),
    ),

    # Foreigner, national
    _StringExtensionField(
        name='speaker_nationality',
        vocabulary_factory='matem.event.NationalityExpositor',
        # default=1,
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Speaker Nationality'),
            description=_(u'Select Mexican if the speaker was born in Mexico'),
            i18n_domain='matem.event',
        ),
    ),

    _LinesExtensionField(
        name='type_event',
        # vocabulary_factory='matem.event.TypeEvent',
        vocabulary=atapi.DisplayList((
            ('researcher', _(u'Researcher')),
            ('rhuman', _(u'Human Resource Training')),
            ('divulgation', _(u'Divulgation')),
        )),
        widget=atapi.MultiSelectionWidget(
            format='checkbox',
            label=_(u'Event Type'),
            description=_(u'Select the event type. You can select one o more'),
            i18n_domain='matem.event',
        ),
        multiValued=True,
    ),
    # _StringExtensionField(
    #     name='type_event',
    #     vocabulary_factory='matem.event.TypeEvent',
    #     widget=atapi.MultiSelectionWidget(
    #         format='checkbox',
    #         label=_(u'Event Type'),
    #         description=_(u'Select the event type. You can select one o more'),
    #         i18n_domain='matem.event',
    #     ),
    # ),


    _StringExtensionField(
        name='researchTopic',
        widget=atapi.InAndOutWidget(
            label=_(u'Researcher Topics'),
            description=_(u'Select the Research Topics. For more information go to the offical page <a href=\"http://www.ams.org/msc\">AMS</a>'),
            i18n_domain='matem.event',
            checkbox_bound=1,
            visible={'view': 'invisible'},
            modes=("edit"),
        ),
        allowed_types=('FSDSpecialty', ),
        vocabulary_factory='imatem.person.specialties',
        multiValued=True,
        relationship='researchTopicOf',
    ),

    _StringExtensionField(
        name='canceled',
        widget=atapi.BooleanWidget(
            label=_(u'Canceled Event'),
            description=_(u'Select if the event was canceled'),
            i18n_domain='matem.event',
        ),
    ),
]


class MatemEventExtender(object):
    """ Adapter that adds matem fields to Person
    """
    component.adapts(IATEvent)
    interface.implements(IOrderableSchemaExtender, ISchemaModifier)

    _fields = BasicSchema

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields

    def getOrder(self, original):
        default = original['default']
        idx = default.index('description')

        default.remove('isIMember')
        default.insert(idx, 'isIMember')
        default.remove('internal_speaker')
        default.insert(idx + 1, 'internal_speaker')

        default.remove('speaker')
        default.insert(idx + 2, 'speaker')
        default.remove('institution')
        default.insert(idx + 3, 'institution')
        default.remove('speaker_nationality')
        default.insert(idx + 4, 'speaker_nationality')
        default.remove('type_event')
        default.insert(idx + 5, 'type_event')

        return original

    def fiddle(self, schema):
        schema.changeSchemataForField('attendees', 'categorization')
        schema.changeSchemataForField('eventUrl', 'categorization')
        schema.changeSchemataForField('contactName', 'categorization')
        schema.changeSchemataForField('contactEmail', 'categorization')
        schema.changeSchemataForField('contactPhone', 'categorization')
        description = schema['description']
        description.widget.visible = {'edit': 'invisible'}

        # Hide the administrative tabs for non-Managers
        for hideme in ['categorization', 'dates', 'creators', 'settings']:
            for fieldName in schema.getSchemataFields(hideme):
                fieldName.widget.visible = {'edit': 'invisible'}
        return schema


@grok.subscribe(ATEvent, IObjectCreatedEvent)
def object_created(context, event):
    """
    """
    seminar = context.getFolderWhenPortalFactory().aq_parent
    context.setLocation(seminar.location)
    context.setSubject(seminar.subject)

    try:
        context.REQUEST
    except AttributeError:
        context.REQUEST = {}

    wholeday = context.REQUEST.get('wholeDay', False)
    ajax = context.REQUEST.get('ajax_load', None)

    if ajax is None:
        dt = DateTime()
        date = '%s %s:00 %s' % (dt.Date(), seminar.start, dt.timezone())
        context.REQUEST['startDate'] = DateTime(date)
        date = '%s %s:00 %s' % (dt.Date(), seminar.end, dt.timezone())
        context.REQUEST['endDate'] = DateTime(date)

    dt = context.REQUEST.get('startDate', None)

    if isinstance(dt, DateTime) and wholeday:
        date = '%s %s:00 %s' % (dt.Date(), seminar.start, dt.timezone())
        context.REQUEST['startDate'] = DateTime(date)

    dt = context.REQUEST.get('endDate', None)
    if isinstance(dt, DateTime) and wholeday:
        date = '%s %s:00 %s' % (dt.Date(), seminar.end, dt.timezone())
        context.REQUEST['endDate'] = DateTime(date)


@grok.subscribe(ATEvent, IObjectAddedEvent)
def object_added(context, event):
    """
    """

    member_value = context.isIMember
    if member_value == 'yes':
        context.speaker = None
        context.institution = None
    else:
        context.internal_speaker = None


@grok.subscribe(ATEvent, IObjectModifiedEvent)
def object_modified(context, event):
    """
    """
    member_value = context.isIMember
    if member_value == 'yes':
        context.speaker = None
        context.institution = None
    else:
        context.internal_speaker = None


@indexer(ATEvent)
def getSpeaker(self):
    member_value = getattr(self, 'isIMember', None)
    if member_value == 'yes':
        rid = getattr(self, 'internal_speaker', None)
        if rid:
            portal_catalog = getToolByName(getSite(), 'portal_catalog')
            query = {
                'portal_type': 'FSDPerson',
                'id': rid,
            }
            brain = portal_catalog.searchResults(query)
            if brain:
                return brain[0].Title.decode('utf-8')
            return None
        return None

    return getattr(self, 'speaker', None)
    # return self.getWrappedField(self, 'speaker')


@indexer(ATEvent)
def getEventInstitution(self):
    member_value = getattr(self, 'isIMember', None)
    if member_value == 'yes':
        return 'IM-UNAM'
    return getattr(self, 'institution', None)


@indexer(ATEvent)
def isCanceled(self):
    return getattr(self, 'canceled', None)
