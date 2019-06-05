# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope.publisher.interfaces import IRequest
from zope.traversing.interfaces import IPathAdapter
from zope.app.pagetemplate.talesapi import ZopeTalesAPI


class UVCSiteTalesAdapter(grok.Adapter, ZopeTalesAPI):
    """extend the zope implementation by providing additional dublin core """
    grok.provides(IPathAdapter)
    grok.context(IRequest)
    grok.name('uvcsite')

    @property
    def homefolder(self):
        hf_url = uvcsite.IGetHomeFolderUrl(self.context).getURL()
        return hf_url
