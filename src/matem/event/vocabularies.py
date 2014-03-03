# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from matem.fsdextender.users import get_users_as_brains
from matem.event import _


def Weekdays(context):
    """Vocabulary for Weekdays.

    PLEASE NOTE: strftime %w interprets 0 as Sunday unlike the calendar module!

        Note: Context is here a RecordProxy and cannot be used to get the site
              root. zope.i18n.translate seems not to respect the portal
              language.
    """

    # TODO: revisit, use zope.i18n
    # see: http://weblion.psu.edu/chatlogs/%23plone/2012/08/15.txt
    # avoid using:
    # translate = getSite().translate
    # it breaks tests. it's defined in:
    # Products.CMFPlone.skins.plone_scripts.translate.py
    # better use:
    # from zope.i18n import translate
    # translate = getToolByName(getSite(), 'translation_service').translate

    # domain = 'matem.event'
    # items = [
    #     (translate(u'weekday_mon', domain=domain, default=u'Monday'), 0),
    #     (translate(u'weekday_tue', domain=domain, default=u'Tuesday'), 1),
    #     (translate(u'weekday_wed', domain=domain, default=u'Wednesday'), 2),
    #     (translate(u'weekday_thu', domain=domain, default=u'Thursday'), 3),
    #     (translate(u'weekday_fri', domain=domain, default=u'Friday'), 4),
    #     (translate(u'weekday_sat', domain=domain, default=u'Saturday'), 5),
    #     (translate(u'weekday_sun', domain=domain, default=u'Sunday'), 6),
    # ]

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
    res = get_users_as_brains(getSite(), sortable=True, person_classification=['investigadores', 'posdoc', 'becarios'])

    for r in res:
        title = (r.lastName + ', ' + r.firstName).encode('utf-8')
        items.append((title, r.UID))

    #value, token, título
    #items = [SimpleTerm(i[0], i[1], i[0]) for i in items]
    items = [SimpleTerm(i[1], str(i[1]), i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(PersonVocabulary, IVocabularyFactory)


def PeriodicitySeminar(context):

    # translate = getToolByName(getSite(), 'translation_service').translate

    # domain = 'matem.event'
    items = [
        (_(u'Weekly'), 1),
        (_(u'Biweekly'), 2),
        (_(u'Monthtly'), 3),
        # (translate(u'periodicity_weekly', domain=domain, default=u'Weekly'), 1),
        # (translate(u'periodicity_fortnightly', domain=domain, default=u'Fortnightly'), 2),
        # (translate(u'periodicity_monthtly', domain=domain, default=u'Monthtly'), 3),
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











