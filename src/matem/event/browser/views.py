# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from collective.plonetruegallery.browser.views.galleryview import GalleryView
from datetime import datetime
from datetime import timedelta
from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from plone import api
from plone.app.discussion.interfaces import IConversation
from plone.app.portlets.portlets.rss import RSSFeed
from Products.CMFCore.utils import getToolByName
from Products.Collage.browser.views import BaseTopicView
from Products.Collage.browser.views import BaseView
from Products.Five import BrowserView
from operator import itemgetter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory


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

        local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(self.context)
        if not ('Editor' in local_roles or 'Manager' in local_roles):
            return nationality

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


    def getVirtual_link(self):
        return getattr(self.context, 'virtual_link', None)

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
        self.matcuerfeed = IMRSSFeed('https://www.matcuer.unam.mx/RSS/', 100)
        self.matcuerfeed.update()
        self.oaxfeed = IMRSSFeed('http://oaxaca.matem.unam.mx/RSS/index.xml', 100)
        self.oaxfeed.update()

    @property
    def portal_catalog(self):
        """."""
        return getToolByName(getSite(), 'portal_catalog')


    def semanaryActivities(self):
        today = DateTime().earliestTime()
        start_date = today + 1
        end_date = today.latestTime() + 9

        foldercu = self.pathcu()
        brainscu = self.criteriaActivities(start_date, end_date, foldercu[0:2])
        brainsuj = self.criteriaActivities(start_date, end_date, self.pathjur())

        special  = api.content.get(path='/actividades/actividades-especiales')
        divulgacion = api.content.get(path='/divulgacion')
        brainss = self.criteriaActivities(start_date, end_date, special)
        disemination = self.criteriaActivities(start_date, end_date, divulgacion)
        cinig = self.criteriaActivities(start_date, end_date, api.content.get(path='/cinig-im'))
        return {
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y'),
            'brainscu': brainscu,
            'brainsjur': brainsuj,
            'matcuerrss': self.semanaryRSS(self.matcuerfeed, start_date, end_date),
            'oaxrss': self.semanaryRSS(self.oaxfeed, start_date, end_date),
            'brainss': brainss,
            'disemination': disemination,
            'cinig': cinig,
        }


    def isActive(self, congress, start_date, end_date):

        if congress.end < start_date:
            return False
        elif congress.start > end_date:
            # return False
            obj = congress.getObject()
            objdict = obj.__dict__
            dates = objdict.get('semanarydates', ())
            for itemdates in dates:
                itemdate = itemdates.get('semdate', '')
                if itemdate:
                    effectivedate = DateTime(itemdate, datefmt='MX')
                    if effectivedate >= start_date and effectivedate <= end_date:
                        return True

            return False

        return True


    def criteriaActivities(self, start_date, end_date, folders=None):

        query = {
            'portal_type': 'Event',
            'end': {'query': [start_date, ], 'range': 'min'},
            'start': {'query': [end_date, ], 'range': 'max'},
            'review_state': 'external',
            'sort_on': 'start',
            'isCanceled': False,
        }

        if folders is not None:
            if not isinstance(folders, list):
                folders = [folders]
            paths = ['/'.join(i.getPhysicalPath()) for i in folders]
            query['path'] = {'query': paths}

        return self.portal_catalog.searchResults(query)


    def pathcu(self):
        return [
            api.content.get(path='/actividades/coloquio'),
            api.content.get(path='/actividades/seminarios'),
            api.content.get(path='/actividades/actividades-especiales/cu'),
            api.content.get(path='/divulgacion'),
            api.content.get(path='/cinig-im/cinig-imunam')]


    def pathjur(self):
        return [api.content.get(path='/juriquilla/actividades')]


    def weekActivities(self):
        start_date = DateTime().earliestTime()
        end_date = start_date.latestTime() + 7

        brainsuj = self.criteriaActivities(start_date, end_date, self.pathjur())

        return {
            'brainsjur': brainsuj,
            'matcuerrss': self.semanaryRSS(self.matcuerfeed, start_date, end_date),
            'oaxrss': self.semanaryRSS(self.oaxfeed, start_date, end_date),
        }

    # agenda
    def upcomingActivities(self):
        start_date = DateTime()
        end_date = start_date.latestTime() + 365

        foldercu = self.pathcu()
        brainscu = self.criteriaActivities(start_date, end_date, foldercu[0:2])
        brainsuj = self.criteriaActivities(start_date, end_date, self.pathjur())
        special  = api.content.get(path='/actividades/actividades-especiales')
        divulgacion = api.content.get(path='/divulgacion')
        cinig = self.criteriaActivities(start_date, end_date, api.content.get(path='/cinig-im'))
        brainss = self.criteriaActivities(start_date, end_date, [special, divulgacion])

        return {
            'brainscu': brainscu,
            'brainsjur': brainsuj,
            'matcuerrss': self.semanaryRSS(self.matcuerfeed, start_date, end_date),
            'oaxrss': self.semanaryRSS(self.oaxfeed, start_date, end_date),
            'special': brainss,
            'cinig': cinig,
        }


    def tvActivities(self):
        start_date = DateTime().earliestTime()
        end_date = start_date.latestTime()

        brainscu = self.criteriaActivities(start_date, end_date, self.pathcu())
        brainsuj = self.criteriaActivities(start_date, end_date, self.pathjur())

        return {
            'brainscu': brainscu,
            'brainsjur': brainsuj,
            'matcuerrss': self.semanaryRSS(self.matcuerfeed, start_date, end_date),
            'oaxrss': self.semanaryRSS(self.oaxfeed, start_date, end_date),
        }

    def specialActivities(self):
        start_date = DateTime().earliestTime()
        end_date = start_date.latestTime()

        ucim  = api.content.get(path='/actividades/actividades-especiales/cuernavaca')
        ujim  = api.content.get(path='/actividades/actividades-especiales/juriquilla')
        uoim  = api.content.get(path='/actividades/actividades-especiales/oaxaca')

        campuses = {
            'Cuernavaca': self.criteriaActivities(start_date, end_date, ucim),
            'Juriquilla': self.criteriaActivities(start_date, end_date, ujim),
            'Oaxaca': self.criteriaActivities(start_date, end_date, uoim)}

        sactivities = []
        for campus, brains in campuses.iteritems():
            for item in brains:
                data = {}
                data['startf'] = self.date_speller(item.start)
                data['date'] = item.start
                data['expositor'] = item.getSpeaker
                data['title'] = item.pretty_title_or_id()
                data['location'] = item.location
                data['hour'] = str(data['startf']['hour']) + ':' + str(data['startf']['minute'])  + ' hrs.'
                value = ''
                if item.Subject:
                    value = item.Subject[0]
                data['seminarytitle'] = value
                data['campus'] = campus
                sactivities.append(data)

        return sactivities


    def unionActivities(self, cuer, jur, oax, specialActivities):

        union = []


        for item in cuer:
            data = {}
            data['startf'] = self.date_speller(item['updated'])
            data['date'] = item['updated']
            data['expositor'] = item.get('speaker', '')
            data['title'] = item.get('title', '')
            data['location'] = item.get('location', '')
            data['hour'] = str(data['startf']['hour']) + ':' + str(data['startf']['minute'])  + ' hrs.'
            data['seminarytitle'] = item.get('seminarytitle', '')
            data['campus'] = 'Cuernavaca'
            union.append(data)

        for item in jur:
            data = {}
            data['startf'] = self.date_speller(item.start)
            data['date'] = item.start
            data['expositor'] = item.getSpeaker
            data['title'] = item.pretty_title_or_id()
            data['location'] = item.location
            data['hour'] = str(data['startf']['hour']) + ':' + str(data['startf']['minute'])  + ' hrs.'
            value = ''
            if item.Subject:
                value = item.Subject[0]
            data['seminarytitle'] = value
            data['campus'] = 'Juriquilla'
            union.append(data)

        for item in oax:
            data = {}
            data['startf'] = self.date_speller(item['updated'])
            data['date'] = item['updated']
            data['expositor'] = item.get('speaker', '')
            data['title'] = item.get('title', '')
            data['location'] = item.get('location', '')
            data['hour'] = str(data['startf']['hour']) + ':' + str(data['startf']['minute'])  + ' hrs.'
            data['seminarytitle'] = item.get('seminarytitle', '')
            data['campus'] = 'Oaxaca'
            union.append(data)

        mergedlist = union + specialActivities
        # aux = [(x, x['date'], x['campus']) for x in union]
        aux = [(x, x['date'], x['campus']) for x in mergedlist]
        aux_sorted = sorted(aux, key=itemgetter(1, 2))
        newunion = [y[0] for y in aux_sorted]

        # return union
        return newunion

    def classstyleCU(self, items):
        if len(items) > 2:
            return 'rotated'

        return 'notrotated'

    def classstyle(self, items):
        if len(items) > 2:
            return 'rotated'

        return 'notrotated'

    def fontSize(self, lenTitle):
        if lenTitle < 54:
            return 'sizeGfont'
        if lenTitle < 109:
            return 'sizeMfont'

        return 'sizeSfont'


    def imgPosters(self):
        atopic = api.content.get(path='/inicio/1/1/posters')
        return atopic.queryCatalog()


    def posterTitle(self, brain):
        ftoday = datetime.today().date() # - timedelta(days=days_to_subtract)
        start_date = brain.start
        end_date = brain.end
        numberday = ftoday.weekday()
        sem_start_date = ftoday - timedelta(days=numberday)
        sem_end_date = ftoday + timedelta(days=6-numberday)

        sdate = datetime(start_date.year(), start_date.month(), start_date.day()).date()
        fdate = datetime(end_date.year(), end_date.month(), end_date.day()).date()
        if fdate < sem_start_date:
            return "Próximas actividades"
        elif sdate > sem_end_date:
            return "Próximas actividades"

        return "Actividades de la semana"


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

        if dend.JulianDay() > dstart.JulianDay():
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
            if 'juriquilla' in self.request['ACTUAL_URL']:
                # must be url activities
                return 'http://www.matem.unam.mx/juriquilla'
            else:
                return 'http://www.matem.unam.mx/juriquilla/actividades'
        if 'juriquilla' in self.request['ACTUAL_URL']:
            return 'http://www.matem.unam.mx'
        else:
            return 'http://www.matem.unam.mx/actividades/allactivitiesview'


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
                if item['updated'] >= date and item['updated'] <= date + 7:
                    ritems.append(item)
                elif item['updated']._hour + 1 >= date._hour and item['updated'] <= date + 7:
                    ritems.append(item)
        return ritems

    def getFancyDate(self, date):
        month_name = {
            'Jan.': 'enero',
            'Feb.': 'febrero',
            'Mar.': 'marzo',
            'Apr.': 'abril',
            'May': 'mayo',
            'June': 'junio',
            'July': 'julio',
            'Aug.': 'agosto',
            'Sep.': 'septiembre',
            'Oct.': 'octubre',
            'Nov.': 'noviembre',
            'Dec.': 'diciembre'
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
            if 'juriquilla' in self.request['ACTUAL_URL']:
                return 'http://paginas.matem.unam.mx/oaxaca/'
            else:
                return 'http://paginas.matem.unam.mx/oaxaca/actividades/'
        if 'juriquilla' in self.request['ACTUAL_URL']:
            return 'http://www.matcuer.unam.mx/'
        else:
            return 'http://www.matcuer.unam.mx/actividades/'


class IMRSSFeed(RSSFeed):
    """an RSS feed"""

    def _buildItemDict(self, item):
        link = item.links[0].get('href', None)
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
