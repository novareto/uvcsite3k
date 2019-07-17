import zope.interface
import zope.component


class ICatalogDeployment(zope.component.interfaces.IObjectEvent):
    pass


@zope.interface.implementer(ICatalogDeployment)
class CatalogDeployment(zope.component.interfaces.ObjectEvent):
    pass
