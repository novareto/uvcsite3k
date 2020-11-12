import grok
import uvcsite.interfaces
import uvcsite.content.interfaces

from abc import ABC, abstractmethod
from grokcore.component import queryOrderedSubscriptions
from uvcsite.content.meta import default_name
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.security.interfaces import IPrincipal


def get_product_registrations(principal, discard_unavailable=False):
    for sub in queryOrderedSubscriptions(
            principal, uvcsite.content.interfaces.IProductRegistration):
        if not discard_unavailable or sub.available():
            yield sub


@implementer(uvcsite.content.interfaces.IProductRegistration)
class ProductRegistration(ABC, grok.Subscription):
    grok.context(IPrincipal)
    grok.baseclass()

    key = None
    inNav = True

    @abstractmethod
    def available(self) -> bool:
        """Availability computation.
        """

    @property
    def title(self):
        return grok.title.bind().get(self)

    @abstractmethod
    def factory(self, *args, **kwargs):
        """Content factory.
        """

    def create(self, container=None):
        if not self.key:
            # This product can't be persisted in a homefolder.
            return

        if container is None:
            container = uvcsite.interfaces.IHomeFolder(self.context)
            if container is None:
                application = getSite()
                manager = uvcsite.interfaces.IHomeFolderManager(application)
                container = manager.create(
                    uvcsite.interfaces.IMasterUser(self.principal).id)

        if self.key not in container:
            if self.factory() is not None:
                productfolder = container[self.key] = self.factory()
                uvcsite.log('Create ProductFolder %s' % self.key)
                return productfolder
