import grok

class PP(grok.Permission):
    grok.name('uvc.VC')

class View(grok.Permission):
    grok.name('uvc.ViewContent')


class Add(grok.Permission):
    grok.name('uvc.AddContent')


class Edit(grok.Permission):
    grok.name('uvc.EditContent')


class User(grok.Role):
    grok.name('uvc.User')
    grok.permissions(
        'zope.View'
    )


class AccessHomeFolder(grok.Permission):
    grok.name('uvc.AccessHomeFolder')


class HomeFolderUser(grok.Role):
    grok.name('uvc.HomeFolderUser')
    grok.permissions(
        AccessHomeFolder
    )


class Editor(grok.Role):
    grok.name('uvc.Editor')
    grok.permissions(
        View,
        PP,
        Add,
        Edit,
        AccessHomeFolder)
