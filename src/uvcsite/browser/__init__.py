from grok import baseclass, View as BaseView
from grok.interfaces import IGrokView
from grok.components import ViewSupportMixin
from grokcore.layout import Page as BasePage
from megrok.z3ctable import TablePage
from zeam.form.base import Form, Fields
from zope.interface import implementer
from grokcore.view.util import url
from grokcore.site.util import getApplication
import grokcore.message


class MenuItem:
    """Replace me by a meaningful class"""


@implementer(IGrokView)
class GrokView(ViewSupportMixin):
    pass


class View(BaseView):
    baseclass()


class Page(GrokView, BasePage):
    baseclass()


class TablePage(GrokView, TablePage):
    baseclass()


class Form(Form):
    baseclass()

    def application_url(self, name=None, data={}):
        """Return the URL of the nearest enclosing `grok.Application`.
        """
        return url(self.request, getApplication(), name=name, data=data)

    def flash(self, message, type='message'):
        """Send a short message to the user.
        """
        grokcore.message.send(message, type=type, name='session')
