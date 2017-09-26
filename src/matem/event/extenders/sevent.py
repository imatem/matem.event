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
        vocabulary_factory='matem.event.NationalityExpositor',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Speaker Nationality'),
            description=_(u'Select Mexican if the speaker was born in Mexico'),
            i18n_domain='matem.event',
        ),
    ),
)) + event.ATEventSchema.copy()


schemata.finalizeATCTSchema(SpecialSchema, moveDiscussion=False)


class ISEvent(Interface):
    """Special Event marker interface"""

# class SEvent(MatemEventExtender):
class SEvent(event.ATEvent):

    implements(ISEvent)

    meta_type = "ATSEvent"
    schema = SpecialSchema

atapi.registerType(SEvent, PROJECTNAME)
