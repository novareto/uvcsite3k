import collections
import collections.abc
import grokcore.component
import grok

import martian
from martian.util import scan_for_classes
from martian.error import GrokError

import zope.security
from zope.component import queryMultiAdapter, getAdapters 
from grok.interfaces import IGrokView
from zope.interface import Interface, implementer


class IMenu(Interface):
    pass


class IMenuEntry(Interface):
    pass


class menu(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

    @classmethod
    def get_default(cls, component, module=None, **data):
        components = list(scan_for_classes(module, IMenu))
        if len(components) == 0:
            raise GrokError(
                "No module-level menu for %r, please use the "
                "'menu' directive." % (component), component)
        elif len(components) == 1:
            component = components[0]
        else:
            raise GrokError(
                "Multiple possible menus for %r, please use the "
                "'menu' directive."
                % (component), component)
        return component


@implementer(IMenuEntry)
class MenuItem:
    grok.name('base entry')
    grok.baseclass()

    icon = ""
    title = ""
    
    def __init__(self, menu, context, request, view):
        self.context = context
        self.request = request
        self.view = view
        self.menu = menu

    def url(self):
        return None

    def available(self):
        return True

    @property
    def selected(self):
        request_url = self.request.getURL()
        url = self.url()
        normalized_action = url
        if not url:
            return False
        if url.startswith('@@'):
            normalized_action = self.action[2:]
        if request_url.endswith('/'+normalized_action):
            return True
        if request_url.endswith('/++view++'+normalized_action):
            return True
        if request_url.endswith('/@@'+normalized_action):
            return True
        if request_url == url:
            return True
        if request_url.endswith('/@@index'):
            if request_url[:-8] == url:
                return True
        return False


@implementer(IMenu)
class Menu(collections.abc.Iterable):
    grok.name('base menu')
    grok.context(Interface)
    grok.provides(IMenu)
    grok.baseclass()

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def available(self):
        return True
    
    def __iter__(self):
        entries = grokcore.component.sort_components((
            e for name, e in getAdapters(
                (self, self.context, self.request, self.view), IMenuEntry)))

        for e in entries:
            e.__parent__ = self
            if zope.security.canAccess(e, 'available') and e.available():
                yield e
            else:
                import pdb
                pdb.set_trace()

    def update(self):
        self.entries = list(iter(self))


class MenuRenderer(grok.ContentProvider, collections.abc.Iterable):
    grok.baseclass()

    bound_menus = tuple()

    def __iter__(self):
        for name in self.bound_menus:
            menu = queryMultiAdapter(
                (self.context, self.request, self.view), IMenu, name=name)
            menu.__parent__ = self.view
            if menu is not None and zope.security.canAccess(menu, 'available'):
                menu.update()                
                yield name, menu
                
                
    def update(self):
        self.menus = collections.OrderedDict(iter(self))
