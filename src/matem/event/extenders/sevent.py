# -*- coding: utf-8 -*-
from matem.event import _
from matem.event.config import PROJECTNAME
from Products.Archetypes import atapi
from Products.Archetypes.atapi import StringField
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content import schemata
from zope.interface import Interface
from zope.interface import implements


SpecialSchema = atapi.Schema((

    StringField(
        name='activityType',
        vocabulary_factory='matem.event.activityType',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Activity Type'),
            # description=_(u'Select Mexican if the speaker was born in Mexico'),
            i18n_domain='matem.event',
        ),
        required=True,
    ),

    # StringField(
    #     name='responsable',
    #     widget=atapi.StringWidget(
    #         label=_(u'Responsable'),
    #         # description=_(u'Type the Speaker Name'),
    #         i18n_domain='matem.event',
    #         size=60,
    #     ),
    #     required=True,
    # ),

)) + event.ATEventSchema.copy()

# SpecialSchema.changeSchemataForField('contactName', 'default')
# SpecialSchema['contactName'].widget.visible = {'edit': 'visible'}
# SpecialSchema.changeSchemataForField('contactName', 'default')
# SpecialSchema.moveField('contactName', after='activityType')
schemata.finalizeATCTSchema(SpecialSchema, moveDiscussion=False)

SpecialSchema.changeSchemataForField('location', 'default')
SpecialSchema.moveField('location', before='startDate')
SpecialSchema.changeSchemataForField('contactName', 'default')
SpecialSchema.moveField('contactName', after='activityType')




# SpecialSchema.moveField('contactName', after='description')
# SpecialSchema.changeSchemataForField('contactName', 'default')
# SpecialSchema.moveField('startDate', after='description')


class ISEvent(Interface):
    """Special Event marker interface"""

# class SEvent(MatemEventExtender):
class SEvent(event.ATEvent):

    implements(ISEvent)

    meta_type = "ATSEvent"
    schema = SpecialSchema

    # def fiddle(self, schema):

    #     import pdb; pdb.set_trace()
    #     pass
    #     import pdb; pdb.set_trace()
    #     schema.changeSchemataForField('contactName', 'default')
    # #     # schema.changeSchemataForField('attendees', 'categorization')
    # #     # schema.changeSchemataForField('eventUrl', 'categorization')
    # #     # schema.changeSchemataForField('contactName', 'categorization')
    # #     # schema.changeSchemataForField('contactEmail', 'categorization')
    # #     # schema.changeSchemataForField('contactPhone', 'categorization')
    # #     # description = schema['description']
    # #     # description.widget.visible = {'edit': 'invisible'}

    # #     # Hide the administrative tabs for non-Managers
    # #     for hideme in ['categorization', 'dates', 'creators', 'settings']:
    # #         for fieldName in schema.getSchemataFields(hideme):
    # #             fieldName.widget.visible = {'edit': 'visible'}
    #     return schema

atapi.registerType(SEvent, PROJECTNAME)
