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


from datetime import datetime


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

    def getTzname(self):
        return 'US/Central'

    def date_speller(self, dt):

        month_name = {'1': 'Enero', '2':'Febrero', '3':'Marzo', '4':'Abril', '5':'Mayo', '6':'Junio', '7':'Julio', '8':'Agosto', '9':'Septiembre', '10':'Octubre', '11':'Noviembre', '12':'Diciembre'}

        minute ="00"
        if dt.minute():
            if len(dt.minute()) > 1:
                minute = dt.minute()



        ret = { 'year':dt.year(),
                'month':month_name[str(dt.month())][:3],
                'day':dt.day(),
                'hour':dt.hour(),
                'minute': minute,
                'second':int(dt.second()),
                'tz': dt.timezone(),
        }

        return ret

    def getEventDescription(self, brain):
        obj = brain.getObject()
        description = ''
        return description

    # def formatted_date(self, dt):

    #     item_date item/start/pCommon|nothing;
    #     date_s python:item_date and item_date.split(' ') or '';
    #     fancy_date python:date_s and date_s[1].replace(',', '') +' de '+ month_name[date_s[0]] + ', ' +  date_s[3] + ' ' + date_s[4] + '.' or '';
                                


    ###################################################################################
    # #app.event functions
    # def date_speller(self, dt):
    #     """Return a dictionary with localized and readably formatted date parts.

    #     """
    #     context = self.context
    #     dt = self.DT(dt)
    #     util = getToolByName(context, 'translation_service')
    #     dom = 'plonelocales'

    #     def zero_pad(num):
    #         return '%02d' % num

    #     date_dict = dict(
    #         year=dt.year(),

    #         month=util.translate(
    #             util.month_msgid(dt.month()),
    #             domain=dom, context=context
    #         ),

    #         month_abbr=util.translate(
    #             util.month_msgid(dt.month(), 'a'),
    #             domain=dom, context=context
    #         ),

    #         wkday=util.translate(
    #             util.day_msgid(dt.dow()),
    #             domain=dom, context=context
    #         ),

    #         wkday_abbr=util.translate(
    #             util.day_msgid(dt.dow(), 'a'),
    #             domain=dom, context=context
    #         ),

    #         day=dt.day(),
    #         day2=zero_pad(dt.day()),

    #         hour=dt.hour(),
    #         hour2=zero_pad(dt.hour()),

    #         minute=dt.minute(),
    #         minute2=zero_pad(dt.minute()),

    #         second=dt.second(),
    #         second2=zero_pad(dt.second())
    #     )
    #     return date_dict

    # def DT(self, dt, exact=False):
    #     """Return a Zope DateTime instance from a Python datetime instance.

    #     :param dt: Python datetime, Python date, Zope DateTime instance or string.
    #     :param exact: If True, the resolution goes down to microseconds. If False,
    #                   the resolution are seconds. Defaul is False.
    #     :type exact: Boolean
    #     :returns: Zope DateTime
    #     :rtype: Zope DateTime

    #     """
    #     def _adjust_DT(DT, exact):
    #         if exact:
    #             ret = DT
    #         else:
    #             ret = DateTime(
    #                 DT.year(),
    #                 DT.month(),
    #                 DT.day(),
    #                 DT.hour(),
    #                 DT.minute(),
    #                 int(DT.second()),
    #                 DT.timezone()
    #             )
    #         return ret

    #     tz = self.default_timezone(getSite())
    #     ret = None
    #     if self.is_datetime(dt):
    #         zone_id = getattr(dt.tzinfo, 'zone', tz)
    #         #tz = validated_timezone(zone_id, tz)
    #         pytz.timezone(timezone).zone
    #         second = dt.second
    #         if exact:
    #             second += dt.microsecond / 1000000.0
    #         ret = DateTime(
    #             dt.year, dt.month, dt.day,
    #             dt.hour, dt.minute, second,
    #             tz
    #         )
    #     elif is_date(dt):
    #         ret = DateTime(dt.year, dt.month, dt.day, 0, 0, 0, tz)
    #     elif isinstance(dt, DateTime):
    #         # No timezone validation. DateTime knows how to handle it's zones.
    #         ret = _adjust_DT(dt, exact=exact)
    #     else:
    #         # Try to convert by DateTime itself
    #         ret = _adjust_DT(DateTime(dt), exact=exact)
    #     return ret




    # def default_timezone(fallback='UTC'):
    #     """ Retrieve the timezone from the server.
    #         Default Fallback: UTC

    #         :param fallback: A fallback timezone identifier.
    #         :type fallback: string

    #         :returns: A timezone identifier.
    #         :rtype: string

    #         >>> from plone.event.utils import default_timezone
    #         >>> import os
    #         >>> import time
    #         >>> timetz = time.tzname
    #         >>> ostz = 'TZ' in os.environ.keys() and os.environ['TZ'] or None

    #         >>> os.environ['TZ'] = "Europe/Vienna"
    #         >>> default_timezone()
    #         'Europe/Vienna'

    #         Timezone from time module
    #         >>> os.environ['TZ'] = ""
    #         >>> time.tzname = ('CET', 'CEST')
    #         >>> default_timezone()
    #         'CET'

    #         Invalid timezone
    #         >>> os.environ['TZ'] = "PST"
    #         >>> default_timezone()
    #         'UTC'

    #         Invalid timezone with defined fallback
    #         >>> os.environ['TZ'] = ""
    #         >>> time.tzname = None
    #         >>> default_timezone(fallback='CET')
    #         'CET'

    #         Restore the system timezone
    #         >>> time.tzname = timetz
    #         >>> if ostz:
    #         ...     os.environ['TZ'] = ostz
    #         ... else:
    #         ...     del os.environ['TZ']

    #     """

    #     timezone = None
    #     if 'TZ' in os.environ.keys():
    #         # Timezone from OS env var
    #         timezone = os.environ['TZ']
    #     if not timezone:
    #         # Timezone from python time
    #         zones = time.tzname
    #         if zones and len(zones) > 0:
    #             timezone = zones[0]
    #         else:
    #             # Default fallback = UTC
    #             logger.warn("Operating system's timezone cannot be found. "
    #                         "Falling back to UTC.")
    #     return validated_timezone(timezone, fallback)


    # def is_datetime(value):
    #     """Checks, if given value is a datetime.

    #     :param value: The value to check.
    #     :type value: object
    #     :returns: True, if value is a datetime (and not a date), false otherwise.
    #     :rtype: Boolean

    #     >>> from plone.event.utils import is_datetime
    #     >>> from datetime import datetime, date
    #     >>> is_datetime(date.today())
    #     False
    #     >>> is_datetime(datetime.now())
    #     True
    #     >>> is_datetime(42)
    #     False
    #     """
    #     return type(value) is datetime



    ###################################################################################


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

