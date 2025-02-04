from plone import api
from zope.publisher.browser import BrowserView

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility


class SeminarsFolderView(BrowserView):
    """ Displays seminars conteined in this folder
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    
    def seminaries(self):
        seminaries = {'active':[], 'notactive': []}
        list_contents = self.context.listFolderContents(contentFilter={"portal_type" : "matem.event.seminar"})
        # seminar = list_contents[0]
        # import pdb; pdb.set_trace()
        start = DateTime()
        end = DateTime() - 180
        for seminar in list_contents:
            query = {}
            # has_query = getattr(seminar, 'buildQuery', None)

            # if has_query:
            #   query = seminar.buildQuery()
            # else:
            query['path'] = {
                'query': '/'.join(seminar.getPhysicalPath()),
                'depth': 2
            }
            query['Type'] = ('Event',)
            
            # upcomingEvents
            # query['end'] = {'query': start, 'range': 'min'}
            # pastEvents
            # query['start'] = {'query': end, 'range': 'max'}

            query['start'] = {'query': end, 'range': 'min'}
            # query['sort_on'] = 'end'
            # query['sort_order'] = 'reverse'
            # query.update(kw)
            cat = getToolByName(seminar, 'portal_catalog')
            result = cat(**query)
            if result:
                seminaries['active'].append(seminar)
            else:
                seminaries['notactive'].append(seminar)
        
        return seminaries
    

    def getDayTitle(self, seminar):
        value = seminar.day
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Weekdays')(seminar).by_value
        return vocabulary[value].title
        