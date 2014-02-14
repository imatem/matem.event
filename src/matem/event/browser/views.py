# -*- coding: utf-8 -*-

from Products.Collage.browser.views import BaseTopicView

class IMStandardTopicView(BaseTopicView):
    pass
    #title = _(u'IM Standard')

class IMEventView(BaseTopicView):

    def getSpeaker(self):
        return getattr(self.context, 'speaker', None)

    def getEventInstitution(self):
        return getattr(self.context, 'institution', None)