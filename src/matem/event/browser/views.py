# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Collage.browser.views import BaseTopicView
from zope.component.hooks import getSite


class IMStandardTopicView(BaseTopicView):
    def filterTopics(self, topics):
        cu = []
        juriquilla = []
        for topic in topics:
            subject = topic.Subject
            if 'Juriquilla' in subject:
                juriquilla.append(topic)
            else:
                cu.append(topic)
        return{'CU': cu, 'Juriquilla': juriquilla}


class IMEventView(BaseTopicView):

    def getSpeaker(self):
        member_value = self.context.isIMember
        if member_value == 'yes':
            rid = self.context.internal_speaker
            if rid:
                portal_catalog = getToolByName(getSite(), 'portal_catalog')
                query = {
                    'portal_type': 'FSDPerson',
                    'id': rid,
                }
                return portal_catalog.searchResults(query)[0].Title

            return None

        return self.context.speaker
        # return getattr(self.context, 'speaker', None)

    def getEventInstitution(self):
        member_value = self.context.isIMember
        if member_value == 'yes':
            return 'IM-UNAM'
        return self.context.institution
        # return getattr(self.context, 'institution', None)

    def isCanceled(self):
        return getattr(self.context, 'canceled', None)
