# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from megrok.pagetemplate import PageTemplate
from zope import interface, component, viewlet
from zope.pagetemplate.interfaces import IPageTemplate

grok.templatedir('templates')


class HelpManager(grok.ViewletManager):
    """ ViewletManager für HilfeSeiten
    """
    grok.context(interface.Interface)
    grok.name('uvc.hilfen')

    def getHelpPages(self):
        return [v for v in self.viewlets if IHelpPage.providedBy(v)]

    def getViewlets(self):
        return [v for v in self.viewlets if not IHelpPage.providedBy(v)]

    def render(self):
        template = component.getMultiAdapter(
            (self, self.request), IPageTemplate)
        return template()


class HelpManagerTemplate(PageTemplate):
    grok.view(HelpManager)


class Help(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(interface.Interface)
    grok.order(9999)

    def render(self):
        helpmanager = component.getMultiAdapter(
            (self.context, self.request, self.view),
            viewlet.interfaces.IViewletManager,
            name=u'uvc.hilfen')
        helpmanager.update()
        return helpmanager.render()


class IHelpPage(interface.Interface):
    pass


@interface.implementer(IHelpPage)
class HelpPage(grok.Viewlet):
    grok.baseclass()
    grok.viewletmanager(HelpManager)

    def update(self):
        self.response = self.request.response

    def namespace(self):
        return {'settings_overrides': {
            'input_encoding': 'utf-8',
            'output_encoding': 'unicode',
            'stylesheet': '',
            'stylesheet_path': None,
            'embed_stylesheet': 0,
        }}
