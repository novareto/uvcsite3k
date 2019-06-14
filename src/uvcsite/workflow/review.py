import grok
import uvcsite.browser
import uvcsite.workflow
import uvcsite.permissions
import uvcsite.interfaces
import uvcsite.browser.layout.slots.interfaces

from hurry.workflow.interfaces import IWorkflowState
from megrok.z3ctable import table, Column
from uvcsite.auth.interfaces import ICOUser
from zope import interface


class ReviewViewlet(grok.Viewlet):
    grok.viewletmanager(uvcsite.browser.layout.slots.interfaces.IAboveContent)
    grok.context(interface.Interface)
    grok.baseclass()

    def available(self):
        if (len(self.values) > 0 and
            not ICOUser.providedBy(self.request.principal)):
            return True
        return False

    def update(self):
        self.homefolder = uvcsite.interfaces.IHomeFolder(self.request)
    
    @property
    def values(self):
        results = []
        if self.homefolder:
            interaction = self.request.interaction
            for productfolder in self.homefolder.values():
                if not productfolder.__name__.startswith('__'):
                    if interaction.checkPermission(
                            'uvc.ViewContent', productfolder):
                        results = [x for x in productfolder.values()
                                   if IWorkflowState(x).getState() == uvcsite.workflow.State.REVIEW]
        return results

    def render(self):
        url = self.view.url(self.homefolder)
        
        return (
            u"<p class='alert'> Sie haben ({}) " +
            u"Dokumente in Ihrer <a href='{}/review_list'>ReviewList</a>.</p>"
        ).format(len(self.values), url)


class ReviewList(uvcsite.browser.TablePage):
    grok.name('review_list')
    grok.require(uvcsite.permissions.Edit)
    grok.baseclass()

    check = uvcsite.permissions.View

    @property
    def values(self):
        results = []
        homefolder = uvcsite.getHomeFolder(self.request)
        if homefolder:
            interaction = self.request.interaction
            for productfolder in homefolder.values():
                if not productfolder.__name__.startswith('__'):
                    if interaction.checkPermission(self.check, productfolder):
                        results = [x for x in productfolder.values()
                                   if IWorkflowState(x).getState() == \
                                          uvcsite.workflow.State.REVIEW]
        return results


class ModifiedColumn(Column):
    grok.name('modified')
    grok.context(interface.Interface)
    header = u"Freigeben"
    weight = 100
    table(ReviewList)

    def renderCell(self, item):
        url = grok.url(self.request, item, name="publish")
        return "<a href='%s'> Freigeben </a>" % url
