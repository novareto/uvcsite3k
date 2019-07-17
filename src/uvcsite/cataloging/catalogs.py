import grok
import zope.interface
import uvcsite.interfaces
import uvcsite.content
import hurry.workflow
import zope.dublincore.interfaces

from zope.component.interfaces import ObjectEvent, IObjectEvent
from uvcsite.cataloging.events import ICatalogDeployment


class IApplicationContent(zope.interface.Interface):

    type = zope.interface.Attribute('Content type')
    state = zope.interface.Attribute('Workflow state')
    modification_date = zope.interface.Attribute('Workflow state')
    creation_date = zope.interface.Attribute('Creation date')
    creator = zope.interface.Attribute('Creator')


@zope.interface.implementer(IApplicationContent)
class ApplicationContent(grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)

    @property
    def type(self):
        return self.context.__class__.__name__

    @property
    def state(self):
        wfstate = hurry.workflow.interfaces.IWorkflowState(self.context)
        return wfstate.getState()

    @property
    def modification_date(self):
        dates = zope.dublincore.interfaces.IDCTimes(self.context)
        return dates.modified

    @property
    def creation_date(self):
        dates = zope.dublincore.interfaces.IDCTimes(self.context)
        return dates.created

    @property
    def creator(self):
        info = zope.dublincore.interfaces.IDCExtended(self.context)
        return info.creators[0]


class WorkflowCatalog(grok.Indexes):
    grok.context(IApplicationContent)
    grok.name('workflow_catalog')
    grok.site(uvcsite.interfaces.IUVCSite)
    grok.install_on(ICatalogDeployment)

    type = grok.index.Field()
    state = grok.index.Field()
    creator = grok.index.Field()
    modification_date = grok.index.Datetime()
    creation_date = grok.index.Datetime()
