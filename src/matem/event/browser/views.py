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
        try:
            member_value = self.context.isIMember
        except AttributeError:
            member_value = 'no'
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
        try:
            member_value = self.context.isIMember
        except AttributeError:
            member_value = 'no'
        if member_value == 'yes':
            return 'IM-UNAM'
        return self.context.institution
        # return getattr(self.context, 'institution', None)

    def isCanceled(self):
        return getattr(self.context, 'canceled', None)

    def getEvetType(self):

        etypes = []
        values = getattr(self.context, 'type_event', None)
        if values:
            vocabulary = self.context.getField('type_event').Vocabulary(self.context)
            translation_service = getSite().translation_service
            for value in filter(None, values):
                langvalue = translation_service.translate(vocabulary.getValue(
                    value),
                    domain="matem.event",
                    target_language=self.context.REQUEST.LANGUAGE).encode('utf-8')

                etypes.append(langvalue)
        return etypes

    def getNationality(self):
        nationality = None
        value = getattr(self.context, 'speaker_nationality', None)
        if value:
            vocabulary = self.context.getField('speaker_nationality').Vocabulary(self.context)
            translation_service = getSite().translation_service
            nationality = translation_service.translate(vocabulary.getValue(
                int(value)),
                domain="matem.event",
                target_language=self.context.REQUEST.LANGUAGE).encode('utf-8')

        return nationality
        # return getattr(self.context, 'speaker_nationality', None)
