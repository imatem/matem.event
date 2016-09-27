from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface
from zope import schema

from OFS.SimpleItem import SimpleItem
# from Products.statusmessages.interfaces import IStatusMessage

# from plone.app.contentrules import PloneMessageFactory
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm


class ICategorizationAction(Interface):
    """Interface for the configurable aspects of a categorization action.

    This is also used to create add and edit forms, below.
    """

    # message = schema.TextArea(title=_(u"Label Categorization"),
    #                           description=_(u"This Label add to categorization object"),
    #                           required=True)

    message = schema.TextLine(title=_(u"Label Categorization"),
                              description=_(u"This Label add to categorization object"),
                              required=True)

    # message_type = schema.Choice(title=_(u"Message type"),
    #                              description=_(u"Select the type of message to display."),
    #                              values=("info", "warning", "error"),
    #                              required=True,
    #                              default="info")


class CategorizationAction(SimpleItem):
    """The actual persistent implementation of the notify action element.
    """
    implements(ICategorizationAction, IRuleElementData)

    message = ''
    # message_type = ''

    element = 'matem.actions.Categorization'

    @property
    def summary(self):
        return _(u"The next label will be assigned ${message}", mapping=dict(message=self.message))


class CategorizationActionExecutor(object):
    """The executor for this action.

    This is registered as an adapter in configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, ICategorizationAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        label = self.element.message
        obj = self.event.object
        # ('Foo',)
        self.event.object.setSubject(label)



        # request = self.context.REQUEST
        # message = PloneMessageFactory(self.element.message)
        # message_type = self.element.message_type
        # IStatusMessage(request).addStatusMessage(message, type=message_type)
        return True


class CategorizationAddForm(AddForm):
    """An add form for notify rule actions.
    """
    form_fields = form.FormFields(ICategorizationAction)
    label = _(u"Add Categorization Action")
    description = _(u"A categorization action can add label to content.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = CategorizationAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class CategorizationEditForm(EditForm):
    """An edit form for notify rule actions.

    Formlib does all the magic here.
    """
    form_fields = form.FormFields(ICategorizationAction)
    label = _(u"Edit Categorization Action")
    description = _(u"A categorization action can add label to content.")
    form_name = _(u"Configure element")
