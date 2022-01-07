# -*- coding: utf-8 -*-
from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from Products.Five import BrowserView
from plone.app.portlets.portlets.rss import RSSFeed


class RSSView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.feed = IMRSSFeed('https://www.matcuer.unam.mx/RSS/', 100)
        # self.feed.update()

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


class RSSOaxacaView(RSSView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.feed = IMRSSFeed('http://oaxaca.matem.unam.mx/RSS/index.xml', 100)
        self.feed.update()


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
