# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Collage.browser.views import BrowserView
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite
from zope.contentprovider.interfaces import IContentProvider
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory


class EventsView(BrowserView):

    def upcomingEvents(self, **kw):
        """Show all upcoming events"""

        query = {}
        has_query = getattr(self.context, 'buildQuery', None)
        if has_query:
            query = self.context.buildQuery()
        else:
            query['path'] = {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1
            }
            query['Type'] = ('Event',)

        start = DateTime()
        query['end'] = {'query': start, 'range': 'min'}
        query['sort_on'] = 'start'
        query.update(kw)
        cat = getToolByName(self.context, 'portal_catalog')
        result = cat(**query)
        return result


    def upcomingEventsWithoutcalendar(self, **kw):
        """Show all upcoming events"""

        query = {}
        # has_query = getattr(self.context, 'buildQuery', None)
        # if has_query:
        #     query = self.context.buildQuery()
        # else:
        query['Type'] = ('Event',)
        query['review_state'] = ('external',)

        start = DateTime()
        query['end'] = {'query': start, 'range': 'min'}
        query['sort_on'] = 'start'
        query.update(kw)
        cat = getToolByName(self.context, 'portal_catalog')
        portal_ppath = api.portal.get().getPhysicalPath()
        query['path'] = {
            'query': (
                '/'.join(portal_ppath) + '/seminarios',
                '/'.join(portal_ppath) + '/actividades/coloquio',
                '/'.join(portal_ppath) + '/actividades/actividades-especiales/cu'
            ),
        }
        seminarios = cat(**query)
        return seminarios

    def pastEvents(self, **kw):
        """Show all past events"""
        query = {}
        has_query = getattr(self.context, 'buildQuery', None)

        if has_query:
            query = self.context.buildQuery()
        else:
            query['path'] = {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1
            }
            query['Type'] = ('Event',)

        end = DateTime()
        query['start'] = {'query': end, 'range': 'max'}
        query['sort_on'] = 'end'
        query['sort_order'] = 'reverse'
        query.update(kw)
        cat = getToolByName(self.context, 'portal_catalog')
        result = cat(**query)
        return result

    def render_filter(self):
        provider = queryMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, 'eventfilter')
        if provider is None:
            return ''
        provider.update()
        return provider.render()

    def viewAbovecontent(self):
        local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(getSite())
        if 'Manager' in local_roles:
            return 'enable_border'
        return 'disable_border'

    def getTzname(self):
        return 'US/Central'

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

    def getEventDescription(self, brain):
        description = ''
        return description

    def factory_item(self):
        menu = getUtility(IBrowserMenu, name='plone_contentmenu_factory')
        items = menu.getMenuItems(self.context, self.request)
        if items:
            return items[0]
        return None

    def isOneDay(self, dstart, dend):

        if dend.JulianDay() > dstart.JulianDay():
            return True
        return False
