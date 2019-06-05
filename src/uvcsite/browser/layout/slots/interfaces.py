import zope.interface


class IPageTop(zope.interface.Interface):
    """Marker For the area that sits at the top of the page.
    """


class ITabs(zope.interface.Interface):
    """Marker for the action tabs.
    """


class IAboveContent(zope.interface.Interface):
    """Marker For the area that sits above the page body.
    """


class IBelowContent(zope.interface.Interface):
    """Marker For the area that sits under the page body.
    """


class IHeaders(zope.interface.Interface):
    """Marker For Headers
    """


class IToolbar(zope.interface.Interface):
    """Marker for Toolbar
    """


class IFooter(zope.interface.Interface):
    """
    """


class IBeforeActions(zope.interface.Interface):
    """
    """


class IExtraInfo(zope.interface.Interface):
    """
    """


__all__ = [
    "IAboveContent",
    "IBeforeActions",
    "IBelowContent",
    "IExtraInfo",
    "IFooter",
    "IHeaders",
    "IPageTop",
    "ITabs",
    "IToolbar",
    ]
