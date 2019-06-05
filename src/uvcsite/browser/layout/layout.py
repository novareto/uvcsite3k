import grok
import grokcore.layout
import zope.interface


from zope.container.interfaces import IContainer
from zope.traversing.browser import absoluteURL


grok.templatedir('templates')


class Layout(grokcore.layout.Layout):
    grok.context(zope.interface.Interface)
    grok.name('')

    def update(self):
        super().update()
        self.base = absoluteURL(self.context, self.request)
        if IContainer.providedBy(self.context) and self.base[:-1] != '/':
            self.base = self.base + '/'
        self.view.update()
