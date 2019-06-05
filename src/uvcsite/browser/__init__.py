from grok import baseclass, View as BaseView
from grok.interfaces import IGrokView
from grok.components import ViewSupportMixin
from grokcore.layout import Page as BasePage
from megrok.z3ctable import TablePage
from zeam.form.base import Form, Fields
from zope.interface import implementer


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
