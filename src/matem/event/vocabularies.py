# -*- coding: utf-8 -*-

from matem.event import _
from matem.fsdextender.users import get_users_as_brains
from zope.component.hooks import getSite
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def Weekdays(context):
    """Vocabulary for Weekdays.

    PLEASE NOTE: strftime %w interprets 0 as Sunday unlike the calendar module!

        Note: Context is here a RecordProxy and cannot be used to get the site
              root. zope.i18n.translate seems not to respect the portal
              language.
    """
    items = [
        (_(u'Monday'), 0),
        (_(u'Tuesday'), 1),
        (_(u'Wednesday'), 2),
        (_(u'Thursday'), 3),
        (_(u'Friday'), 4),
        (_(u'Saturday'), 5),
        (_(u'Sunday'), 6),
    ]
    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(Weekdays, IVocabularyFactory)


def PersonVocabulary(context):
    """Vocabulary factory for all people
    """
    items = []
    res = get_users_as_brains(
        getSite(),
        sortable=True,
        person_classification=['investigadores', 'posdoc', 'becarios'])
    for r in res:
        title = (r.lastName + ', ' + r.firstName).encode('utf-8')
        items.append((title, r.UID))
    items = [SimpleTerm(i[1], str(i[1]), i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(PersonVocabulary, IVocabularyFactory)


def PeriodicitySeminar(context):
    items = [
        (_(u'Weekly'), 1),
        (_(u'Biweekly'), 2),
        (_(u'Monthtly'), 3),
    ]

    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(PeriodicitySeminar, IVocabularyFactory)


def Months(context):

    items = [
        (_(u'January'), 1),
        (_(u'February'), 2),
        (_(u'March'), 3),
        (_(u'April'), 4),
        (_(u'May'), 5),
        (_(u'June'), 6),
        (_(u'July'), 7),
        (_(u'August'), 8),
        (_(u'September'), 9),
        (_(u'October'), 10),
        (_(u'November'), 11),
        (_(u'December'), 12),
    ]

    #value, token, título
    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(Months, IVocabularyFactory)
