#-*- coding: utf-8 -*-
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
from matem.event import _
# from DateTime import DateTime
# from DateTime.interfaces import DateError
from zope.i18n import translate
# from zope.i18nmessageid import Message
from zope.interface import Invalid


class InternalSpeakerValidator:
    """
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        request = kwargs['REQUEST']
        if request.form['isIMember'] == 'yes':
            if not value:
                kwargs['errors']['internal_speaker'] = _(u'Validation failed: Internal Author is required, please correct.')
                # return
                # raise Invalid(_(u'Validation failed: Internal Author is required, please correct.'))
                # return translate(_("Validation failed: Internal Author is required, please correct."), domain='matem.event', context=request)

        return True


class ExternalSpeakerValidator:
    """
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        request = kwargs['REQUEST']
        if request.form['isIMember'] == 'no':
            if not value:
                return translate(_("Validation failed: External Author is required, please correct."), domain='matem.event', context=request)

        return True