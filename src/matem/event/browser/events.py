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



class EventsView(BrowserView):
    pass
    #title = _(u'IM Standard')


    def upcomingEvents(self, **kw):
        """Show all upcoming events"""
        default = getDefaultPage(self.context)
        context = self.context[default]
        #self.context[default].listCriteria()
        query = context.buildQuery()

        start = DateTime()
        query['end'] = {'query': start, 'range': 'min'}

        query['sort_on'] = 'start'
        
        query.update(kw)

        cat = getToolByName(context, 'portal_catalog')
        result = cat(**query)
        

        return result

    def pastEvents(self, **kw):
        """Show all past events"""
        default = getDefaultPage(self.context)
        context = self.context[default]
        query = context.buildQuery()

        end = DateTime()
        query['start'] = {'query': end, 'range': 'max'}

        query['sort_on'] = 'end'
        query['sort_order'] = 'reverse'

        query.update(kw)

        cat = getToolByName(context, 'portal_catalog')
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



    # def _getEventList(self, start=None, end=None, sort='start', sort_reverse=False, **kw):
    #     #context = self.context
    #     #_args, filters = self._getCriteriaArgs()
    #     default = getDefaultPage(self.context)
    #     context = self.context[default]
    #     #self.context[default].listCriteria()
    #     query = context.buildQuery()

    #     if start is None:
    #         start = DateTime()
    #         query['end'] = {'query': start, 'range': 'min'}
        
    #     if end is None:
    #         end = DateTime()
    #         query['start'] = {'query': end, 'range': 'max'}
        
        

    #     #days = range(start.toordinal(), 
    #     #            (stop + datetime.timedelta(hours=23, minutes=59)).toordinal())

    #     #query['recurrence_days']=days

    #     query['sort_on'] = sort
    #     if sort_reverse:
    #         query['sort_order'] = 'reverse'

    #     query.update(kw)

    #     cat = getToolByName(context, 'portal_catalog')
    #     result = cat(**query)

    #     import pdb; pdb.set_trace( )
        
    #     return result



    # # context = self.context    
    # # request = self.request
    # # _args, filters = self._getCriteriaArgs()
    


    # # def _getEventList(self, start=None, stop=None):

    # #     #import pdb; pdb.set_trace( )

    # #     #def _getEvents(self, start=None, stop=None, **kw):
    # #     kw = _make_zcatalog_query(start, stop, kw)
    # #     tool = cmfutils.getToolByName(self.context, 'portal_calendar')
    # #     portal_types = tool.getCalendarTypes()
    # #     # Any first occurrences:
    # #     event_brains = self._query(portal_type=portal_types, **kw)
    # #     # And then the recurrences:
    # #     if start is None:
    # #         # XXX This is to handle the recurring events in the past events view.
    # #         # This could also likely be improved.
    # #         start = datetime.datetime(1970, 1, 1, 0, 0)
    # #     if stop is None:
    # #         # XXX This is to handle the recurring events in the list view.
    # #         # It should possibly be done some other way, since it will recur to
    # #         # the year 2020 as it is now.
    # #         stop = start + datetime.timedelta(30)
    # #     days = range(start.toordinal(), 
    # #                 (stop + datetime.timedelta(hours=23, minutes=59)).toordinal())
    # #     # XXX How do we make the recurrence story pluggable?
    # #     # This didn't work, because if RecurringEvent is not installed all fails:
    # #     # Maybe we don't need pluggability, we could just require p4a.ploneevent,
    # #     # But at least it should work without it....
    # #     if 'start' in kw:
    # #         del kw['start']
    # #     if 'end' in kw:
    # #         del kw['end']
    # #     recurrences = self._query(portal_type=portal_types, 
    # #                               recurrence_days=days,
    # #                               **kw)
    # #     return tuple((kalends.ITimezonedOccurrence(x) for x in event_brains)) + \
    # #            tuple((kalends.ITimezonedRecurringEvent(x) for x in recurrences))











    #     # ##########################Lo de p4canlendar # ########################
    #     # #provider = IATEvent(self.context)

    #     # # provider = kalends.IEventProvider(self.context)
    #     # # now = datetime.datetime.now()
    #     # # events = list(provider.getOccurrences(start=start, stop=stop, 
    #     # #                                      **self.request.form))

    #     # events = []

    #     # events.sort()
    #     # months = []
    #     # month_info = []
    #     # old_month_year = None
    #     # for event in events:
    #     #     start = event.start
    #     #     month = str(start.month)
    #     #     year = str(start.year)
    #     #     month_year = year+month
    #     #     if month_year != old_month_year:
    #     #         old_month_year = month_year
    #     #         if month_info:
    #     #             months.append(month_info)
    #     #         month_info = {'month': start.month,
    #     #                       'year': start.year,
    #     #                       'month_name': start.strftime("%B"),
    #     #                       'events': []}
    #     #     subject = ''
    #     #     if event._getEvent().Subject():
    #     #         subject = event._getEvent().Subject()[0]
    #     #     event_dict = {'event': event,
    #     #                   'day': start.day,
    #     #                   'title': event.title,
    #     #                   'description': event.description,
    #     #                   'location': event.location,
    #     #                   'url': event.url,
    #     #                   'subject': subject,
    #     #                   'cssclass': self.cssclass(subject),
    #     #                   }
    #     #     month_info['events'].append(event_dict)

    #     # if month_info:
    #     #     months.append(month_info)

    #     # return months

    # # def upcomingEvents(self):
    # #     """Show all upcoming events"""
    # #     now = datetime.datetime.now()
    # #     months = self._getEventList(start=now)
    # #     return self.eventlist(months=months, show_past=False)

    # # def pastEvents(self):
    # #     """Show all past events"""
    # #     now = datetime.datetime.now()
    # #     months = self._getEventList(stop=now)
    # #     months.reverse()
    # #     for month in months:
    # #         month['events'].reverse()
    # #     return self.eventlist(months=months, show_past=True)

