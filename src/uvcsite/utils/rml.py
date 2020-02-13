# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import os.path
import martian


from z3c.rml import rml2pdf
from z3c.rml import pagetemplate

from zope.interface import implementer

from grokcore.view.components import PageTemplate
from grokcore.component import GlobalUtility, name
from grokcore.view.interfaces import ITemplate, ITemplateFileFactory


@implementer(ITemplate)
class RMLTemplate(PageTemplate):
    def setFromString(self, string):
        rml = pagetemplate.RMLPageTemplateFile()
        if martian.util.not_unicode_or_ascii(string):
            raise ValueError(
                "Invalid page template. Page templates must be " "unicode or ASCII."
            )
        rml.write(string)
        self._template = rml

    def setFromFilename(self, filename, _prefix=None):
        filename = os.path.join(_prefix, filename)
        self._template = pagetemplate.RMLPageTemplateFile(filename)

    def get_pdf_value(self, view):
        rml = super(RMLTemplate, self).render(view)
        pdf = rml2pdf.parseString(rml)
        return pdf.getvalue()

    def render(self, view):
        view.response.setHeader("Content-Type", "application/pdf")
        rml = super(RMLTemplate, self).render(view)
        pdf = rml2pdf.parseString(rml)
        return pdf.getvalue()


@implementer(ITemplateFileFactory)
class RMLTemplateFactory(GlobalUtility):
    name("rml")

    def __call__(self, filename, _prefix=None):
        return RMLTemplate(filename=filename, _prefix=_prefix)
