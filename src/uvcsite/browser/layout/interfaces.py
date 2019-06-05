from zope.interface import Interface


class ISubMenu(Interface):
    """ Marker Interface for Sub Menus"""


class IRenderable(Interface):
    """ Marker Interface for MenuItems which render Itself """
