# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import grok

from grok import IDefaultBrowserLayer
from zope.pluggableauth import interfaces
from zope.pluggableauth import factories
from uvcsite.content.principal import Principal


class UVCSitePrincipalFactory(
    factories.AuthenticatedPrincipalFactory, grok.MultiAdapter
):
    grok.adapts(interfaces.IPrincipalInfo, IDefaultBrowserLayer)

    def __call__(self, authentication):
        principal = Principal(
            authentication.prefix + self.info.id, self.info.description
        )
        grok.notify(
            interfaces.AuthenticatedPrincipalCreated(
                authentication, principal, self.info, self.request
            )
        )
        return principal
