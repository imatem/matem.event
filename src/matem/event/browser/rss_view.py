# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.portlets.portlets.rss import RSSFeed
from DateTime import DateTime
from DateTime.interfaces import DateTimeError

class RSSView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.feed = IMRSSFeed('http://www.matcuer.unam.mx/RSS/', 100)
        self.feed.update()

    # @property
    # def initializing(self):
    #     """should return True if deferred template should be displayed"""
    #     feed = self._getFeed()
    #     if not feed.loaded:
    #         return True
    #     if feed.needs_update:
    #         return True
    #     return False

    @property
    def feedAvailable(self):
        """checks if the feed data is available"""
        return self.feed

    # def isCurrentHour(self):
    #     """Return true if this object represents a date/time
    #     that falls within the current hour, in the context
    #     of this object\'s timezone representation.
    #     """
    #     t=time()
    #     gmt=safegmtime(t+_tzoffset(self._tz, t))
    #     return (gmt[0]==self._year and gmt[1]==self._month and
    #             gmt[2]==self._day and gmt[3]==self._hour)


    def items(self):

        ritems = []
        date = DateTime()
        for item in self.feed.items:
            if item.get('updated', ''):
                # import pdb; pdb.set_trace( )
                if item['updated'] >= date and item['updated']<= date + 15:
                    ritems.append(item)


        return ritems
        # return self.feed.items


    def getFancyDate(self, date):
        month_name = {
            'Jan.': 'Enero',
            'Feb.':'Febrero',
            'Mar.':'Marzo',
            'Apr.':'Abril',
            'May':'Mayo',
            'June':'Junio',
            'July':'Julio',
            'Aug.':'Agosto',
            'Sep.':'Septiembre',
            'Oct.':'Octubre',
            'Nov.':'Noviembre',
            'Dec.':'Diciembre'
        }

        datetime = date and date.pCommon() or ''
        if datetime:
            date_s = datetime.split(' ')
            return date_s[1].replace(',', '') +' de '+ month_name[date_s[0]] + ', ' +  date_s[3] + ' ' + date_s[4] + '.' or ''

        return datetime


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

