# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from uvcsite.content.productregistration import getProductRegistrations
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocabulary(terms):
    """FIX ME
    """
    return SimpleVocabulary(
        [SimpleTerm(value, token, title) for value, token, title in terms])


@grok.provider(IContextSourceBinder)
def vocab_berechtigungen(context):
    return SimpleVocabulary([
        SimpleTerm(reg.folderURI, reg.folderURI, reg.linkname)
        for id, reg in getProductRegistrations()
        if reg.asRole is True
    ])
