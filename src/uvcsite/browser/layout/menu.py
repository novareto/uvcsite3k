import collections
import collections.abc
import grokcore.viewlet.util
import grok
from zope.component import queryMultiAdapter, getAdapters 
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from grok.interfaces import IGrokView
from zope.interface import Interface, implementer


class IMenu(Interface):
    pass


class IMenuEntry(Interface):
    pass


@implementer(IMenuEntry)
class MenuItem(grok.MultiAdapter):
    grok.name('base entry')
    grok.adapts(Interface, IDefaultBrowserLayer, IGrokView, IMenu)
    grok.baseclass()

    icon = ""
    title = ""
    
    def __init__(self, context, request, view, menu):
        self.context = context
        self.request = request
        self.view = view
        self.menu = menu

    def url(self):
        return None

    def available(self):
        return True


@implementer(IMenu)
class Menu(grok.MultiAdapter, collections.abc.Iterable):
    grok.name('base menu')
    grok.adapts(Interface, IDefaultBrowserLayer, IGrokView)
    grok.baseclass()

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def available(self):
        return True

    def __iter__(self):
        for i in grokcore.viewlet.util.sort_components(
            (e for name, e in getAdapters(
                (self.context, self.request, self.view, self), IMenuEntry)
             if e.available())):
            yield i

    def update(self):
        self.entries = list(iter(self))


class MenuRenderer(grok.ContentProvider, collections.abc.Iterable):
    grok.baseclass()

    bound_menus = tuple()

    def __iter__(self):
        for name in self.bound_menus:
            menu = queryMultiAdapter(
                (self.context, self.request, self.view), IMenu, name=name)
            if menu is not None and menu.available():
                menu.update()
                yield name, menu

    def update(self):
        self.menus = collections.OrderedDict(iter(self))
