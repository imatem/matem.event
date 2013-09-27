# -*- coding: utf-8 -*-

from Products.Collage.browser.views import BaseTopicView
from Products.Collage.utilities import CollageMessageFactory as _

class IMStandardTopicView(BaseTopicView):
    title = _(u'IM Standard')
