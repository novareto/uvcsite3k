# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite.interfaces
import zope.app.appsetup.interfaces

from uvcsite.content.interfaces import IProductRegistration
from zope.component import getAdapters
from zope.pluggableauth.factories import Principal


def createProductFolders(principal=None):
    interaction = zope.security.management.getInteraction()
    if interaction is None:
        # We don't have a valid interaction, let's get out of here.
        return

    request = interaction.participations[0]
    if not principal:
        principal = request.principal
    for name, pr in getAdapters((principal, request), IProductRegistration):
        pr.createInProductFolder()


@grok.subscribe(uvcsite.interfaces.IHomeFolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    createProductFolders(principal)
