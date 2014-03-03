from Products.Collage.browser.views import BrowserView
#from Products.Collage.browser.views import BaseTopicView
#import datetime
from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
#from Products.ATContentTypes.interfaces import IATEvent
#from zope.component.hooks import getSite
#from plone.app.layout.navigation.root import getNavigationRootObject
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.defaultpage import getDefaultPage
#from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from zope.component.hooks import getSite
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory



from datetime import datetime


class EventsView(BrowserView):
    #pass
    #title = _(u'IM Standard')

    def upcomingEvents(self, **kw):
        """Show all upcoming events"""

        query = {}
        has_query = getattr(self.context, 'buildQuery', None)

        if has_query:
            query = self.context.buildQuery()
        else:
            query['path'] = {'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1}
            query['Type'] = ('Event',)

        start = DateTime()
        query['end'] = {'query': start, 'range': 'min'}

        query['sort_on'] = 'start'
        
        query.update(kw)

        cat = getToolByName(self.context, 'portal_catalog')
        result = cat(**query)

        return result

    def pastEvents(self, **kw):
        """Show all past events"""


        query = {}
        has_query = getattr(self.context, 'buildQuery', None)

        if has_query:
            query = self.context.buildQuery()
        else:
            query['path'] = {'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1}
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


        # from zope.i18n import translate
        # translate = getToolByName(getSite(), 'translation_service').translate
        #(translate(u'weekday_mon', domain=domain, default=u'Monday'), 0),

        #month_apr
        #import pdb; pdb.set_trace( )

        #month_name = {'1': 'Enero', '2':'Febrero', '3':'Marzo', '4':'Abril', '5':'Mayo', '6':'Junio', '7':'Julio', '8':'Agosto', '9':'Septiembre', '10':'Octubre', '11':'Noviembre', '12':'Diciembre'}

        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Months')(self.context).by_value
        #return vocabulary[value].title

        minute ="00"
        if dt.minute():
            if len(str(dt.minute())) > 1:
                minute = dt.minute()

        ret = { 'year':dt.year(),
                'month':vocabulary[dt.month()].title[:3],
                'day':dt.day(),
                'hour':dt.hour(),
                'minute': minute,
                'second':int(dt.second()),
                'tz': dt.timezone(),
        }

        # ret = { 'year':dt.year(),
        #         'month':month_name[str(dt.month())][:3],
        #         'day':dt.day(),
        #         'hour':dt.hour(),
        #         'minute': minute,
        #         'second':int(dt.second()),
        #         'tz': dt.timezone(),
        # }

        return ret

    def getEventDescription(self, brain):
        obj = brain.getObject()
        description = ''
        return description

    def factory_item(self):

        menu = getUtility(IBrowserMenu, name='plone_contentmenu_factory')
        items = menu.getMenuItems(self.context, self.request)
        if items:
            return items[0]
        return None 