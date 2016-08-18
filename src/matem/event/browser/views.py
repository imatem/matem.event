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
        try:
            self.context.speaker
        except AttributeError:
            return None
        return self.context.speaker
        # return self.context.speaker
        # return getattr(self.context, 'speaker', None)

    def getEventInstitution(self):
        try:
            member_value = self.context.isIMember
        except AttributeError:
            member_value = 'no'
        if member_value == 'yes':
            return 'IM-UNAM'
        try:
            self.context.institution
        except AttributeError:
            return None
        return self.context.institution
        # return self.context.institution
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
                value),
                domain="matem.event",
                target_language=self.context.REQUEST.LANGUAGE).encode('utf-8')

        return nationality
        # return getattr(self.context, 'speaker_nationality', None)


from Acquisition import aq_inner, aq_base
from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.DiscussionTool import DiscussionNotAllowed

from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter

from plone.app.discussion.interfaces import IConversation
from DateTime import DateTime




class IMPageCommentView(BaseTopicView):

    # Methods of
    def can_reply(self):
        return getSecurityManager().checkPermission('Reply to item', aq_inner(self.context))


    def getComments(self, workflow_actions=True):
        """Returns all replies to a content object.

        If workflow_actions is false, only published
        comments are returned.

        If workflow actions is true, comments are
        returned with workflow actions.
        """
        context = aq_inner(self.context)
        conversation = IConversation(context, None)

        if conversation is None:
            return iter([])

        wf = getToolByName(context, 'portal_workflow')

        # workflow_actions is only true when user
        # has 'Manage portal' permission

        def replies_with_workflow_actions():
            # Generator that returns replies dict with workflow actions
            for r in conversation.getThreads():
                comment_obj = r['comment']
                # list all possible workflow actions
                actions = [
                    a for a in wf.listActionInfos(object=comment_obj)
                    if a['category'] == 'workflow' and a['allowed']
                ]
                r = r.copy()
                r['actions'] = actions
                yield r

        def published_replies():
            # Generator that returns replies dict with workflow status.
            for r in conversation.getThreads():
                comment_obj = r['comment']
                workflow_status = wf.getInfoFor(comment_obj, 'review_state')
                if workflow_status == 'published':
                    r = r.copy()
                    r['workflow_status'] = workflow_status
                    yield r

        # Return all direct replies
        lenvalue = len(conversation.objectIds())


        if len(conversation.objectIds()):
            if workflow_actions:
                return replies_with_workflow_actions()
            else:
                return published_replies()

    def format_time(self, time):
        # We have to transform Python datetime into Zope DateTime
        # before we can call toLocalizedTime.
        util = getToolByName(self.context, 'translation_service')
        zope_time = DateTime(time.isoformat())
        return util.toLocalizedTime(zope_time, long_format=True)
