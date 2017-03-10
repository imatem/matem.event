# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from collective.plonetruegallery.browser.views.galleryview import GalleryView
from DateTime import DateTime
from plone.app.discussion.interfaces import IConversation
from Products.CMFCore.utils import getToolByName
from Products.Collage.browser.views import BaseTopicView
from Products.Five import BrowserView
from zope.component.hooks import getSite

from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
# from matem.event.browser.rss_view import IMRSSFeed

from Products.Collage.browser.views import BaseView
from plone.app.portlets.portlets.rss import RSSFeed
from DateTime.interfaces import DateTimeError



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


class IMGalleryView(GalleryView):
    pass


class SemanaryView(BrowserView):

    def __init__(self, context, request):
        """Initialize view."""
        self.context = context
        self.request = request
        self.matcuerfeed = IMRSSFeed('http://www.matcuer.unam.mx/RSS/', 100)
        self.matcuerfeed.update()
        self.oaxfeed = IMRSSFeed('http://paginas.matem.unam.mx/oaxaca/RSS/index.xml', 100)
        self.oaxfeed.update()

    @property
    def portal_catalog(self):
        """."""
        return getToolByName(getSite(), 'portal_catalog')

    def semanaryActivities(self):
        ftoday = DateTime()
        today = DateTime('/'.join([str(ftoday.year()), str(ftoday.month()), str(ftoday.day())]))
        start_date = today + 1
        end_date = today + 7.9999
        query = {
            'portal_type': 'Event',
            'end': {'query': [start_date, ], 'range': 'min'},
            'start': {'query': [end_date, ], 'range': 'max'},
            'review_state': 'external',
            'sort_on': 'start',
            'isCanceled': False,

        }

        brains = self.portal_catalog.searchResults(query)

        brainscu = []
        brainsjur = []

        for brain in brains:
            if 'Juriquilla' in brain.Subject:
                brainsjur.append(brain)
            else:
                brainscu.append(brain)

        iso_start = start_date.ISO().split('-')
        day_start = iso_start[2].split('T')

        iso_end = end_date.ISO().split('-')
        day_end = iso_end[2].split('T')

        return {
            'brainscu': brainscu,
            'start_date': '/'.join([day_start[0], iso_start[1], iso_start[0]]),
            'end_date': '/'.join([day_end[0], iso_end[1], iso_end[0]]),
            'matcuerrss': self.semanaryRSS(self.matcuerfeed, start_date, end_date),
            'oaxrss': self.semanaryRSS(self.oaxfeed, start_date, end_date),
            'brainsjur': brainsjur,
        }

    def date_speller(self, dt):
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Months')(self.context).by_value
        minute = "00"
        if dt.minute():
            if len(str(dt.minute())) > 1:
                minute = dt.minute()

        ret = {
            'year': dt.year(),
            'month': translate(vocabulary[dt.month()].title, domain='matem.event', context=self.request)[:3].lower(),
            'day': dt.day(),
            'hour': dt.hour(),
            'minute': minute,
            'second': int(dt.second()),
            'tz': dt.timezone(),
        }
        return ret

    def semanaryRSS(self, feed, start_date, end_date):

        ritems = []
        # date = DateTime()
        for item in feed.items:
            if item.get('updated', ''):
                if item['updated'] < start_date:
                    continue
                if item['updated'] >= start_date and item['updated'] <= end_date:
                    ritems.append(item)
                elif item['updated']._hour + 1 >= start_date._hour and item['updated'] <= end_date:
                    ritems.append(item)
        return ritems

    def isOneDay(self, dstart, dend):

        if dend - dstart >= 2:
            return True
        return False

# ##########
# classes that unify the events in the site and rss service
# ##########

class IMSiteTopicView(BaseTopicView):

    def cstyle(self, ptitle):
        if 'Juriquilla' in ptitle:
            return 'jurheader-color'
        return 'cuheader-color'

    def topicstyle(self, ptitle):
        if 'Juriquilla' in ptitle:
            return 'jurborder-color'
        return 'cuborder-color'

    def topicHome(self, ptitle):
        if 'Juriquilla' in ptitle:
            return ''
        return 'http://www.matem.unam.mx'


class RSSTopicsView(BaseView):
    title = u'RSSlink_topics'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # self.feed = IMRSSFeed('http://paginas.matem.unam.mx/oaxaca/RSS/index.xml', 100)
        self.feed = IMRSSFeed(self.context.remote_url(), 100)
        self.feed.update()

    @property
    def feedAvailable(self):
        """checks if the feed data is available"""
        return self.feed

    def hasFeed(self):
        if self.items():
            return True
        return False

    def items(self):

        ritems = []
        date = DateTime()
        for item in self.feed.items:
            if item.get('updated', ''):
                if item['updated'] < date:
                    continue
                if item['updated'] >= date and item['updated'] <= date + 14:
                    ritems.append(item)
                elif item['updated']._hour + 1 >= date._hour and item['updated'] <= date + 14:
                    ritems.append(item)
        return ritems

    def getFancyDate(self, date):
        month_name = {
            'Jan.': 'Enero',
            'Feb.': 'Febrero',
            'Mar.': 'Marzo',
            'Apr.': 'Abril',
            'May': 'Mayo',
            'June': 'Junio',
            'July': 'Julio',
            'Aug.': 'Agosto',
            'Sep.': 'Septiembre',
            'Oct.': 'Octubre',
            'Nov.': 'Noviembre',
            'Dec.': 'Diciembre'
        }

        datetime = date and date.pCommon() or ''
        if datetime:
            date_s = datetime.split(' ')
            return date_s[1].replace(',', '') + ' de ' + month_name[date_s[0]] + ', ' + date_s[3] + ' ' + date_s[4] + '.' or ''

        return datetime

    def cstyle(self):
        if 'oaxaca' in self.context.remote_url():
            return 'oaxheader-color'

        return 'cuerheader-color'

    def topicstyle(self):
        if 'oaxaca' in self.context.remote_url():
            return 'oaxborder-color'
        return 'cuerborder-color'

    def topicHome(self):
        if 'oaxaca' in self.context.remote_url():
            return 'http://paginas.matem.unam.mx/oaxaca/'
        return 'http://www.matcuer.unam.mx/'


class IMRSSFeed(RSSFeed):
    """an RSS feed"""

    def _buildItemDict(self, item):
        link = item.links[0]['href']
        itemdict = {
            'title': item.title,
            'url': link,
            'summary': item.get('description', ''),
            'speaker': item.get('dc_speaker', ''),
            'institution': item.get('dc_institution', ''),
            'seminarytitle': item.get('dc_seminarytitle', ''),
            'location': item.get('dc_location', ''),
        }
        if hasattr(item, "updated"):
            try:
                itemdict['updated'] = DateTime(item.updated)
            except DateTimeError:
                # It's okay to drop it because in the
                # template, this is checked with
                # ``exists:``
                pass

        return itemdict







