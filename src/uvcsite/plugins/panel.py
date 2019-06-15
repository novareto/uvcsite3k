import grok
import json
import zope.interface
import zope.component
import uvcsite.browser

import zope.schema
from zeam.form.base import FAILURE
from zope.component import getMultiAdapter
from zope.location import Location, LocationProxy
from zope.container.interfaces import IReadContainer
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from uvcsite.plugins.flags import States, ResultTypes
from uvcsite.plugins.components import Result, IPlugin, IComplexPlugin


grok.templatedir('templates')


@zope.interface.implementer(IReadContainer, IDCDescriptiveProperties)
class PluginsPanel(Location):

    title = "Plugins"
    description = "Application plugins management"

    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent

    def __iter__(self):
        plugins = zope.component.getUtilitiesFor(IPlugin)
        for name, plugin in plugins:
            yield name, LocationProxy(plugin, self, name)

    def __getitem__(self, name):
        plugin = zope.component.queryUtility(IPlugin, name=name)
        if plugin is None:
            raise KeyError(name)
        return LocationProxy(plugin, self, name)

    def __contains__(self, name):
        return zope.component.queryUtility(IPlugin, name=name) is not None

    def get(self, name, default=None):
        try:
            item = self.__getitem__(name)
        except KeyError:
            return default
        return item


class PluginsPanelManagement(uvcsite.browser.Page):
    grok.context(PluginsPanel)
    grok.name('index')
    grok.require('grok.ManageApplications')

    needs_fontawesome = True

    def plugins(self):
        url = self.url(self.context)
        for name, plugin in self.context:
            yield {
                'id': name,
                'title': plugin.title,
                'plugin': plugin,
                'icon': 'fas fa5x fa-' + getattr(plugin, 'fa_icon', 'wrench'),
                'url': '%s/%s' % (url, name)
                }


class JSON(grok.MultiAdapter):
    grok.name('application/json')
    grok.provides(zope.interface.Interface)
    grok.adapts(IPlugin, IDefaultBrowserLayer, Result)

    def __init__(self, plugin, request, result):
        self.plugin = plugin
        self.request = request
        self.result = result
    
    def __call__(self):
        return u'<pre>%s</pre>' % json.dumps(
            self.result.value, indent=4, sort_keys=True)


class plain(grok.MultiAdapter):
    grok.name('text/plain')
    grok.provides(zope.interface.Interface)
    grok.adapts(IPlugin, IDefaultBrowserLayer, Result)

    def __init__(self, plugin, request, result):
        self.plugin = plugin
        self.request = request
        self.result = result
    
    def __call__(self):
        return u'<pre>%s</pre>' % self.result.value

    
class PluginOverview(uvcsite.browser.Form):
    grok.context(IPlugin)
    grok.name('index')
    grok.require('grok.ManageApplications')

    prefix = ""
    fields = uvcsite.browser.Fields()
    needs_fontawesome = True

    @property
    def actions(self):
        return self.context.actions

    def updateForm(self):
        form, action, result = self.updateActions()
        if action is not None:
            self.title = action.title
            if result is not FAILURE:
                assert isinstance(result, Result)
                if result.type is ResultTypes.MESSAGE:
                    self.flash(result.value)
                    if result.redirect:
                        return self.redirect(self.url(self.context))
                else:
                    rendering = getMultiAdapter(
                        (self.context, self.request, result),
                        name=result.type.value)
                    self.result = rendering()
        self.updateWidgets()

    def update(self):
        self.title = None
        self.result = None
        self.status = self.context.status
        self.is_installed = self.status.state == States.INSTALLED


class ComplexPluginOverview(PluginOverview):
    grok.context(IComplexPlugin)
    grok.name('index')
    grok.require('grok.ManageApplications')

    def update(self):
        PluginOverview.update(self)
        self.subplugins = self.context.subplugins


class PluginInfo(grok.ContentProvider):
    grok.name('plugin_info')
    grok.template('plugin_info')
    grok.view(PluginOverview)
    grok.context(IPlugin)


class PluginSubplugins(grok.ContentProvider):
    grok.name('plugin_info')
    grok.template('plugin_subplugins')
    grok.view(PluginOverview)
    grok.context(IComplexPlugin)
