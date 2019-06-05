# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import base64
import grok
import time
import datetime
import uvcsite
import xmlrpclib
from grokcore.chameleon.components import ChameleonPageTemplateFile
from grokcore.chameleon.components import PageTemplateFile

from megrok.z3ctable import Column, table

grok.templatedir('templates')


class Altdaten(uvcsite.TablePage):
    """ """
    grok.baseclass()
    template = ChameleonPageTemplateFile('templates/altdaten.cpt')
    grok.title(u'Alte Dokumente')

    cssClasses = {'table': 'tablesorter'}
    title = u"Alte Dokumente"
    description = u"Hier finden Sie die vor dem 30.Mai.2011 erstellten Unfallanzeigen."

    object_type = ""

    @property
    def values(self):
        raise NotImplementedError


class Title(Column):
    """ """
    grok.name('title')
    table(Altdaten)
    grok.context(uvcsite.IProductFolder)
    header = u"Titel"
    weight = 10

    def renderCell(self, item):
        url = "%s/@@pdf?id=%s" % (self.table.url(), item['id'])
        link = '<a href="%s"> %s </a>' % (url, item['title'])
        return link


class Autor(Column):
    """ """
    grok.name('autor')
    table(Altdaten)
    grok.context(uvcsite.IProductFolder)
    header = u"Erstellt von"
    weight = 20

    def renderCell(self, item):
        return item['Creator']


class Status(Column):
    """ """
    grok.name('status')
    table(Altdaten)
    grok.context(uvcsite.IProductFolder)
    header = u"Status"
    weight = 30

    def renderCell(self, item):
        return item['review_state']


class Datum(Column):
    """ """
    grok.name('datum')
    table(Altdaten)
    grok.context(uvcsite.IProductFolder)
    header = u"Datum"
    weight = 40

    def renderCell(self, item):
        datumString = item['ModificationDate']
        datumFmt = "%Y-%m-%d %H:%M:%S"
        datum = datetime.datetime.fromtimestamp(time.mktime(time.strptime(datumString, datumFmt)))
        datum = datum.strftime("%d.%m.%Y %H:%M:%S")
        return datum


class PDF(grok.View):
    grok.view(Altdaten)
    grok.context(Altdaten)
    grok.baseclass()

    def url(self):
        raise NotImplementedError

    def render(self):
        oid = self.request.get('id')
        principal = self.request.principal.id
        URL = self.url()
        server = xmlrpclib.ServerProxy(URL)
        content = server.asRemotePdf(oid, principal)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=unfallanzeige.pdf')
        return base64.decodestring(content)
