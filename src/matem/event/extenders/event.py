# -*- coding: utf-8 -*-
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from zope import component
from zope import interface
from Products.Archetypes import atapi
from Products.ATContentTypes.content.event import ATEvent
from plone.indexer.decorator import indexer


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
    component.adapts(ATEvent)
    interface.implements(IOrderableSchemaExtender)

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

        return original


@indexer(ATEvent)
def getSpeaker(self):
    return getattr(self, 'speaker', None)
    #return self.getWrappedField(self, 'speaker')


