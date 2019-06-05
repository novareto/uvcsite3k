import grok


class MasterUser(grok.Role):
    grok.name('uvc.MasterUser')
    grok.permissions('uvc.ManageCoUsers')


class ManageCoUsers(grok.Permission):
    grok.name('uvc.ManageCoUsers')
