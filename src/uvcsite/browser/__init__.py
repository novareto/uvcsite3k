from grok import baseclass, View as BaseView, Viewlet, context
from grok.interfaces import IGrokView
from grok.components import ViewSupportMixin
from grokcore.layout import Page as BasePage
from megrok.z3ctable import TablePage
from zeam.form.base import Fields
from zope.interface import implementer
from grokcore.view.util import url
from grokcore.site.util import getApplication
from grokcore.layout.components import LayoutAware
from zeam.form.layout import Form
import grokcore.message
from zope.interface import Interface


class MenuItem(Viewlet):
    """Replace me by a meaningful class"""
    baseclass()
    context(Interface)

    title = u""
    selected = False
    icon = u""

    def render(self):
        return u""
    #render.base_method = True


@implementer(IGrokView)
class GrokView(ViewSupportMixin):
    pass


class View(BaseView):
    baseclass()


class Page(GrokView, BasePage):
    baseclass()


class TablePage(GrokView, TablePage):
    baseclass()


class Form(Form, LayoutAware):
    baseclass()

    def application_url(self, name=None, data={}):
        """Return the URL of the nearest enclosing `grok.Application`.
        """
        return url(self.request, getApplication(), name=name, data=data)

    def flash(self, message, type='message'):
        """Send a short message to the user.
        """
        grokcore.message.send(message, type=type, name='session')
