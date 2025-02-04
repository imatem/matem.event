from plone import api
from zope.publisher.browser import BrowserView

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from plone.i18n.normalizer import idnormalizer as idn
from operator import itemgetter


class SeminarsFolderView(BrowserView):
    """ Displays seminars conteined in this folder
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    
    def seminaries(self):
        seminaries = {'active':[], 'notactive': []}
        list_contents = self.context.listFolderContents(contentFilter={"portal_type" : "matem.event.seminar"})
        start = DateTime()
        end = DateTime() - 180
        for seminar in list_contents:
            query = {}
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
            cat = getToolByName(seminar, 'portal_catalog')
            result = cat(**query)
            if result:
                seminaries['active'].append(seminar)
            else:
                seminaries['notactive'].append(seminar)

        seminarios_juriquilla = api.content.get(path='/juriquilla/actividades/seminarios')
        list_contents_juriquilla = seminarios_juriquilla.listFolderContents(contentFilter={"portal_type" : "matem.event.seminar"})
        for seminar in list_contents_juriquilla:
            query = {}
            query['path'] = {
                'query': '/'.join(seminar.getPhysicalPath()),
                'depth': 2
            }
            query['Type'] = ('Event',)
            query['start'] = {'query': end, 'range': 'min'}
            cat = getToolByName(seminar, 'portal_catalog')
            result = cat(**query)
            if result:
                seminaries['active'].append(seminar)
            else:
                seminaries['notactive'].append(seminar)



        aux = [(sem, idn.normalize(sem.Title())) for sem in seminaries['active']]
        aux_sorted = sorted(aux, key=itemgetter(1))
        actives = [t[0] for t in aux_sorted]

        aux = [(sem, idn.normalize(sem.Title)) for sem in seminaries['notactive']]
        aux_sorted = sorted(aux, key=itemgetter(1))
        notactives = [t[0] for t in aux_sorted]

        # return seminaries
        return {'active': actives, 'notactive': notactives}
    

    def getDayTitle(self, seminar):
        value = seminar.day
        vocabulary = getUtility(IVocabularyFactory, 'matem.event.Weekdays')(seminar).by_value
        return vocabulary[value].title
    

    