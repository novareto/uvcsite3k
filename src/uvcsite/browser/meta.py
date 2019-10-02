import martian
import grokcore.view
import grokcore.viewlet
import grokcore.component
import grokcore.security
import uvcsite.browser.layout.menu

from grokcore.view.meta.views import default_view_name
from grokcore.viewlet.util import make_checker
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class MenuGrokker(martian.ClassGrokker):
    martian.component(uvcsite.browser.layout.menu.Menu)
    martian.directive(grokcore.component.context, default=Interface)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.viewlet.view, default=Interface)
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.security.require, name='permission')

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(MenuGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, view, name,
                permission, **kw):
        # This will be used to support __name__ on the viewlet manager
        factory.__view_name__ = name
        config.action(
            discriminator=('Menu', context, layer, view, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (context, layer, view),
                  uvcsite.browser.layout.menu.IMenu , name))

        config.action(
            discriminator=('protectName', factory),
            callable=make_checker,
            args=(factory, factory, permission, ['available']))
        return True


class MenuItemGrokker(martian.ClassGrokker):
    martian.component(uvcsite.browser.layout.menu.MenuItem)
    martian.directive(uvcsite.browser.layout.menu.menu)
    martian.directive(grokcore.component.context, default=Interface)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.viewlet.view, default=Interface)
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.security.require, name='permission')

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(MenuItemGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, menu, context, layer, view, name,
                permission, **kw):
        # This will be used to support __name__ on the viewlet manager
        factory.__view_name__ = name
        config.action(
            discriminator=('MenuItem', context, layer, view, menu, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (menu, context, layer, view),
                  uvcsite.browser.layout.menu.IMenuEntry , name))

        config.action(
            discriminator=('protectName', factory),
            callable=make_checker,
            args=(factory, factory, permission, ['available']))

        return True
