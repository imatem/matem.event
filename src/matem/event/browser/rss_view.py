# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.portlets.portlets.rss import RSSFeed
# from plone.app.portlets.portlets


class RSSView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.feed = RSSFeed('http://www.matcuer.unam.mx/RSS/', 100)
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

    def items(self):
        return self.feed.items

