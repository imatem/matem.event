# -*- coding: utf-8 -*-

from matem.event import _
from Products.validation.interfaces.IValidator import IValidator
from zope.i18n import translate
from zope.interface import implements


class InternalSpeakerValidator:
    """
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        """
        For add blur attributte
        Products/CMFPlone/skins/plone_ecmascript/inline_validation.js
        $('.field #internal_speaker').live('blur', function () {
            var $input = $(this),
                $field = $input.closest('.field'),
                uid = $field.attr('data-uid'),
                fname = $field.attr('data-fieldname'),
                value = $input.val();

            if ($field && uid && fname) {
                $.post($('base').attr('href') + '/at_validate_field', {uid: uid, fname: fname, value: value}, function (data) {
                    render_error($field, data.errmsg);
                });
            }
        });
        """
        request = kwargs['REQUEST']
        member_value = request.form.get('isIMember', '')
        if member_value == 'yes' and not value:
            return translate(_('Validation failed: Speaker is required, please correct it.'), domain='matem.event', context=request)
            # return _("Validation failed: Speaker is required, please correct it.")

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
        member_value = request.form.get('isIMember', '')
        if member_value == 'no' and not value:
            return translate(_('Validation failed: Speaker is required, please correct it.'), domain='matem.event', context=request)
            # return _("Validation failed: Speaker is required, please correct it.")

        # instance = kwargs.get('instance', None)
        # if instance and instance.isIMember == 'no' and not value:
        #     return _("Validation failed: Speaker is required, please correct it.")

        return True
