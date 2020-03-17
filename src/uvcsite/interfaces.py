import grokcore.site
import grok.interfaces
import zope.interface


class IUVCSite(grokcore.site.IApplication):
    pass


class IHomeFolder(grok.interfaces.IContainer):
    pass


class IHomeFolderManager(zope.interface.Interface):
    pass


class IMyRoles(zope.interface.Interface):
    """Return all allowed Roles in various forms
    """



