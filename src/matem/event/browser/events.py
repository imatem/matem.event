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
                '/'.join(portal_ppath) + '/actividades/actividades-especiales/cu',
                '/'.join(portal_ppath) + '/divulgacion'
            ),
        }
        seminarios = cat(**query)
        return seminarios

    def getActivities(self, activities):
        """ see matem.event.browser.views.semanaryActivities
        """
        act = []
        act.extend(activities['brainscu'])
        act.extend(activities['brainsjur'])
        uc = self.unidadContents(activities['matcuerrss'], 'sede-cuernavaca')
        act.extend(uc)
        uo = self.unidadContents(activities['oaxrss'], 'sede-oaxaca')
        act.extend(uo)
        act.extend(activities['special'])
        return sorted(act, key = lambda i: i['start'])


    def unidadContents(self, activities, campuscode):
        min_dt = DateTime()
        uc = []
        for act in activities:
            start = act['updated']
            if min_dt < start:
                uc.append({
                    'getURL': act['url'],
                    'pretty_title_or_id': act['title'],
                    'start': start,
                    'location': act['location'],
                    'Subject': (act['seminarytitle'],),
                    'getSpeaker': act['speaker'],
                    'getEventInstitution': act['institution'],
                    'isCanceled': False,
                    'campus': campuscode,
                })
        return uc


    def campus_class(self, item):
        cclass = item.get('campus', None)
        if cclass is not None:
            return cclass
        url = item.getURL()
        if '/juriquilla/' in url:
            return 'sede-juriquilla'
        if '/oaxaca/' in url:
            return 'sede-oaxaca'
        if 'cuernavaca' in url:
            return 'sede-cuernavaca'
        return 'sede-cu'

    def campus_name(self, item):
        cclass = item.get('campus', None)
        if cclass is not None:
            if cclass == 'sede-cuernavaca':
                return 'Cuernavaca'
            return 'Oaxaca'
        url = item.getURL()
        if '/juriquilla/' in url:
            return 'Juriquilla'
        if '/oaxaca/' in url:
            return 'Oaxaca'
        if 'cuernavaca' in url:
            return 'Cuernavaca'
        return 'Ciudad Universitaria'

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
        if dend is None:
            return False
        if dend.JulianDay() > dstart.JulianDay():
            return True
        return False
