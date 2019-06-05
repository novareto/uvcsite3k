# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.app.appsetup.product
from dolmen.beaker.utilities import ImmutableDict
from dolmen.beaker.interfaces import ISessionConfig


config = zope.app.appsetup.product.getProductConfiguration('beaker')

if config:

    CONFIG = ImmutableDict(
        data_dir=config.get('session.data_dir', None),
        invalidate_corrupt=True,
        key=config.get('session.key', 'uvcsite.session.id'),
        log_file=None,
        cookie_domain=config.get('session.cookie_domain'),
        secret=config.get('session.secret', 'DolmenRocks'),
        timeout=config.get('session.timeout', 600,),
        type=config.get('session.type', 'cookie'),
        validate_key=config.get('session.validatekey', 'thisCouldBeChanged')
        )

    grok.global_utility(
        CONFIG,
        provides=ISessionConfig,
        direct=True,
        )
