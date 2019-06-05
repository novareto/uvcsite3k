# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import martian


class contenttype(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = None
    validate = martian.validateClass


class productfolder(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = None
    validate = martian.validateText
