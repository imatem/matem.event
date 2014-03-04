# -*- coding: utf-8 -*-
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from DateTime import DateTime
from five import grok
from Products.Archetypes import atapi
from zope.lifecycleevent import IObjectCreatedEvent
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.interfaces import IATEvent
from plone.indexer.decorator import indexer
from zope import component
from zope import interface


class _StringExtensionField(ExtensionField, atapi.StringField):
    '''Any field you can tack on must have ExtensionField as its first subclass
    '''
    pass

BasicSchema = [

    _StringExtensionField(
        name='speaker',
        widget=atapi.StringWidget(
            label=u'Nombre del expositor',
            size=60,
        ),
    ),

    _StringExtensionField(
        name='institution',
        widget=atapi.StringWidget(
            label=u'Institution',
            label_msgid='label_institution',
            i18n_domain='UNAM.imateCVct',
            size=60,
        ),
    ),


    _StringExtensionField('researchTopic',
        widget=atapi.InAndOutWidget(
            label=u'area(s) de trabajo',
            label_msgid='label_researchtopic',
            description=u'Selecccione la(s) area(s) de trabajo. Dudas acerca de la clasificacion y como encontrar una area, acceder a la pagina oficial de la <a href=\"http://www.ams.org/msc\">AMS</a>',
            description_msgid="help_researchtopic",
            i18n_domain='UNAM.imateCVct',
            checkbox_bound=1,
            visible = {'view': 'invisible'},
            modes=("edit"),
        ),
        allowed_types=('FSDSpecialty', ),
        vocabulary_factory='imatem.person.specialties',
        multiValued=True,
        relationship='researchTopicOf',
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
        default.remove('speaker')
        default.insert(idx, 'speaker')
        default.remove('institution')
        default.insert(idx +1, 'institution')

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

    dt = context.REQUEST.get('startDate', None)
    if isinstance(dt, DateTime):
        date = '%s %s:00 %s' % (dt.Date(), seminar.start, dt.timezone())
        context.REQUEST['startDate'] = DateTime(date)

    dt = context.REQUEST.get('endDate', None)
    if isinstance(dt, DateTime):
        date = '%s %s:00 %s' % (dt.Date(), seminar.end, dt.timezone())
        context.REQUEST['endDate'] = DateTime(date)



@indexer(ATEvent)
def getSpeaker(self):
    return getattr(self, 'speaker', None)
    #return self.getWrappedField(self, 'speaker')

@indexer(ATEvent)
def getEventInstitution(self):
    return getattr(self, 'institution', None)


