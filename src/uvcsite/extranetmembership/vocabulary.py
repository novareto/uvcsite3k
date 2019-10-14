# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from uvcsite.utils.shorties import getPrincipal
from uvcsite.content.productregistration import get_product_registrations
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocabulary(terms):
    """FIX ME
    """
    return SimpleVocabulary(
        [SimpleTerm(value, token, title) for value, token, title in terms])


@grok.provider(IContextSourceBinder)
def vocab_berechtigungen(context):
    principal = getPrincipal()
    return SimpleVocabulary((
        SimpleTerm(reg.key, reg.key, reg.title)
        for reg in get_product_registrations(
                principal, discard_unavailable=True)
    ))
