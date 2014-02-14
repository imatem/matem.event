# -*- coding: utf-8 -*-
from Products.Collage.browser.views import BrowserView
import datetime
from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from Products.ATContentTypes.interfaces import IATEvent



class EventsView(BrowserView):
    pass
    #title = _(u'IM Standard')


    def _getEventList(self, start=None, stop=None):

        #import pdb; pdb.set_trace( )

        #provider = IATEvent(self.context)

        # provider = kalends.IEventProvider(self.context)
        # now = datetime.datetime.now()
        # events = list(provider.getOccurrences(start=start, stop=stop, 
        #                                      **self.request.form))

        events = []

        events.sort()
        months = []
        month_info = []
        old_month_year = None
        for event in events:
            start = event.start
            month = str(start.month)
            year = str(start.year)
            month_year = year+month
            if month_year != old_month_year:
                old_month_year = month_year
                if month_info:
                    months.append(month_info)
                month_info = {'month': start.month,
                              'year': start.year,
                              'month_name': start.strftime("%B"),
                              'events': []}
            subject = ''
            if event._getEvent().Subject():
                subject = event._getEvent().Subject()[0]
            event_dict = {'event': event,
                          'day': start.day,
                          'title': event.title,
                          'description': event.description,
                          'location': event.location,
                          'url': event.url,
                          'subject': subject,
                          'cssclass': self.cssclass(subject),
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)

        return months

    def upcomingEvents(self):
        """Show all upcoming events"""
        now = datetime.datetime.now()
        months = self._getEventList(start=now)
        return self.eventlist(months=months, show_past=False)

    def pastEvents(self):
        """Show all past events"""
        now = datetime.datetime.now()
        months = self._getEventList(stop=now)
        months.reverse()
        for month in months:
            month['events'].reverse()
        return self.eventlist(months=months, show_past=True)

    def render_filter(self):
        provider = queryMultiAdapter(
            (self.context, self.request, self), 
            IContentProvider, 'eventfilter')
        if provider is None:
            return ''
        provider.update()
        return provider.render()
