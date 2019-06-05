# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import tempfile
import zope.app.appsetup.product
from reportlab.pdfgen import canvas
from zope.interface import Interface
from repoze.filesafe import create_file


TMPDIR = None
config = zope.app.appsetup.product.getProductConfiguration('tempdir')
if config:
    TMPDIR = config.get('path')


class BaseDataView(grok.View):
    grok.context(Interface)
    grok.baseclass()
    grok.name('basedateview')
    grok.title('basedataview')
    grok.require('uvc.ViewContent')
    content_type = ""

    def getFile(self, fn):
        if fn:
            return create_file(fn, 'w+b', TMPDIR)
        return tempfile.TemporaryFile()

    @property
    def filename(self):
        return grok.title.bind().get(self)

    def update(self, filename=None):
        self.base_file = self.getFile(filename)
        self.generate()

    def create(self, fn):
        """schreibt die Datei weg und schliesst das File"""
        self.update(fn)
        self.base_file.close()

    def genpdf(self):
        return self.generate()

    def generate(self):
        """Methode muss von jedem Konsumenten ausprogrammiert werden,
           weil diese Methode beim Aufruf von der Methode
           update aufgerufen wird."""
        raise NotImplementedError

    def render(self):
        currentfile = self.base_file
        currentfile.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', self.content_type)
        RESPONSE.setHeader('content-length', currentfile)
        RESPONSE.setHeader(
            'content-disposition', 'attachment; filename=%s' % self.filename)
        return currentfile


class BasePDF(BaseDataView):
    grok.baseclass()
    grok.name('pdf')
    grok.title('uvcsite.pdf')
    content_type = "application/pdf"

    def update(self, filename=None):
        self.base_file = self.getFile(filename)
        self.c = canvas.Canvas(self.base_file)
        self.genpdf()
        self.c.save()


class WatermarkPDF(BasePDF):
    grok.baseclass()

    def update(self, filename=None):
        super(WatermarkPDF, self).update(filename=filename)
        self.watermark()


class BaseXML(BaseDataView):
    grok.name('xml')
    grok.title('uvcsite.xml')
    grok.baseclass()
    content_type = "application/xml"
