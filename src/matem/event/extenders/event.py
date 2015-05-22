# -*- coding: utf-8 -*-

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from DateTime import DateTime
from five import grok
from Products.Archetypes import atapi
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectCreatedEvent
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.interfaces import IATEvent
from plone.indexer.decorator import indexer
from zope import component
from zope import interface

from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from matem.event import _


class _StringExtensionField(ExtensionField, atapi.StringField):
    '''Any field you can tack on must have ExtensionField as its first subclass
    '''
    pass

BasicSchema = [

    _StringExtensionField(
        name='isIMember',
        required=True,
        vocabulary_factory='matem.event.isIMember',
        widget=MasterSelectWidget(
            label=_(u'Is the speaker IM Member?'),
            # label_msgid='label_ismember_event',
            description=_(u'Select Yes if the speaker is IM member'),
            # description_msgid='help_ismember_event',
            # Seleccione si el expositor es de la comunidad del IM',
            i18n_domain='matem.event',
            slave_fields=(
                {'name': 'internal_speaker', 'action': 'hide', 'hide_values': ('no',)},
                {'name': 'institution', 'action': 'hide', 'hide_values': ('yes',)},
                {'name': 'speaker', 'action': 'hide', 'hide_values': ('yes',)},
            ),
            # visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),

    _StringExtensionField(
        name='internal_speaker',
        vocabulary_factory='matem.event.speakersVocabulary',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Speaker name'),
            # label_msgid='label_namespeaker_event',
            description=_(u'Select the speaker name'),
            # description_msgid='help_internal_speaker_event',
            i18n_domain='matem.event',
            # label=u'Nombre del expositor',
            # description=u'Seleccione el expositor',
            size=60,
        ),
    ),

    _StringExtensionField(
        name='speaker',
        widget=atapi.StringWidget(
            label=_(u'Speaker name'),
            # label_msgid='label_namespeaker_event',
            description=_(u'Type the Speaker Name'),
            # description_msgid='help_external_speaker_event',
            # label=u'Nombre del expositor',
            i18n_domain='matem.event',
            size=60,
        ),
    ),

    _StringExtensionField(
        name='institution',
        widget=atapi.StringWidget(
            label=_(u'Institution'),
            # label_msgid='label_institution',
            # i18n_domain='UNAM.imateCVct',
            i18n_domain='matem.event',
            size=60,
        ),
    ),

    # Foreigner, national
    _StringExtensionField(
        name='speaker_nationality',
        vocabulary_factory='matem.event.NationalityExpositor',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Speaker Nationality'),
            # label_msgid='label_speaker_nationality_event',
            description=_(u'Select Mexican if the speaker was born in Mexico'),
            # description_msgid='help_speaker_nationality_event',
            # label=u'Nacionalidad del expositor',
            # # label_msgid='label_speaker_origin',
            # description=u'Seleccione la nacionalidad del expositor',
            # i18n_domain='UNAM.imateCVct',
            i18n_domain='matem.event',
        ),
    ),

    _StringExtensionField(
        name='type_event',
        vocabulary_factory='matem.event.TypeEvent',
        widget=atapi.MultiSelectionWidget(
            format='checkbox',
            label=_(u'Event Type'),
            # label_msgid='label_type_event',
            description=_(u'Select the event type. You can select one o more'),
            # description_msgid='help_type_event',
            # label=u'Tipo del Evento',
            # # label_msgid='label_speaker_origin',
            # description=u'Seleccione el (los) tipo(s) de evento(s)',
            # i18n_domain='UNAM.imateCVct',
            i18n_domain='matem.event',
        ),
    ),


    _StringExtensionField(
        name='researchTopic',
        widget=atapi.InAndOutWidget(
            label=_(u'Researcher Topics'),
            # label_msgid='label_researchtopic_event',
            description=_(u'Select the Research Topics. For more information go to the offical page <a href=\"http://www.ams.org/msc\">AMS</a>'),
            # description_msgid='help_researchtopic_event',
            i18n_domain='matem.event',
            # label=u'area(s) de trabajo',
            # label_msgid='label_researchtopic',
            # description=u'Selecccione la(s) area(s) de trabajo. Dudas acerca de la clasificacion y como encontrar una area, acceder a la pagina oficial de la <a href=\"http://www.ams.org/msc\">AMS</a>',
            # description_msgid="help_researchtopic",
            # i18n_domain='UNAM.imateCVct',
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
            # label_msgid='label_status_event',
            description=_(u'Select if the event was canceled'),
            # description_msgid='help_status_event',
            i18n_domain='matem.event',
            # label=u'Evento Cancelado',
            # label_msgid='label_status_event',
            # description=u'Seleccione si el evento fue cancelado',
            # description_msgid="help_status_event",
            # i18n_domain='UNAM.imateCVct',
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


# @grok.subscribe(ATEvent, IObjectAddedEvent)
# def object_added(context, event):
#     if not context.isIMember:
#         return
#     import pdb; pdb.set_trace()




@indexer(ATEvent)
def getSpeaker(self):
    return getattr(self, 'speaker', None)
    #return self.getWrappedField(self, 'speaker')


@indexer(ATEvent)
def getEventInstitution(self):
    return getattr(self, 'institution', None)


@indexer(ATEvent)
def isCanceled(self):
    return getattr(self, 'canceled', None)
