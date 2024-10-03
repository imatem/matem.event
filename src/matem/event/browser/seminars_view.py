from plone import api
from zope.publisher.browser import BrowserView

from DateTime import DateTime

class SeminarsFolderView(BrowserView):
    """ Displays seminars conteined in this folder
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
