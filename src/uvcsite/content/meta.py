# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import martian
import grokcore.component

from martian.error import GrokError
from uvcsite.content import ProductFolder, contenttype, IProductFolder
import zope.component.zcml


def default_name(factory, module=None, **data):
    return factory.__name__.lower()


class ProductFolderGrokker(martian.ClassGrokker):
    martian.component(ProductFolder)
    martian.directive(contenttype)
    martian.directive(grokcore.component.name, get_default=default_name)

    def execute(self, factory, config, contenttype, name):
        if not contenttype:
            raise GrokError("%r must specify which contenttype should "
                            "go into this ProductFolder. Please use the"
                            "direcitve 'contenttype' for it."
                            % factory, factory)

        name = name.capitalize()
        config.action(
            discriminator=('utility', IProductFolder, name),
            callable=zope.component.zcml.handler,
            args=('registerUtility', factory, IProductFolder, name),
            )

        return True
