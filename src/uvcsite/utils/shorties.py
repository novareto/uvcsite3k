# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import pytz
import urllib
import uvcsite
import zope.security

from datetime import datetime, date
from uvcsite.interfaces import IHomeFolder
from zope.authentication.interfaces import IUnauthenticatedPrincipal


def getHomeFolder(request):
    principal = request.principal
    if IUnauthenticatedPrincipal.providedBy(principal):
        return
    return IHomeFolder(principal).homeFolder


def getHomeFolderUrl(request, suffix=""):
    url = uvcsite.IGetHomeFolderUrl(request).getURL(type=suffix)
    if url:
        url = urllib.unquote(url)
    return url


def fmtDateTime(object, fmt="%d.%m.%Y %H:%M:%S"):
    tz = pytz.timezone("Europe/Berlin")
    return object.astimezone(tz).strftime(fmt)


def fmtDate(p_date):
    if p_date is None:
        return ''
    tz = pytz.timezone('Europe/Berlin')
    if isinstance(p_date, datetime):
        if p_date.tzinfo:
            tz = p_date.tzinfo
        p_date = datetime(p_date.year, p_date.month, p_date.day, tzinfo=tz)
        return fmtDateTime(p_date, fmt='%d.%m.%Y')
    if isinstance(p_date, date):
        p_date = datetime(p_date.year, p_date.month, p_date.day, tzinfo=tz)
    if isinstance(p_date, int):
        p_date = str(p_date)
    if isinstance(p_date, str):
        p_date = datetime(
            int(p_date[0:4]), int(p_date[4:6]), int(p_date[6:8]), tzinfo=tz)
    return fmtDateTime(p_date, fmt='%d.%m.%Y')


def fmtZahl(n):
    if isinstance(n, str) or isinstance(n, int):
        r = []
        for i, c in enumerate(reversed(str(n))):
            if i and (not (i % 3)):
                r.insert(0, '.')
            r.insert(0, c)
        return ''.join(r)
    return n


def fmtFloat(f, dp=2):
    if f is None:
        return ''
    assert(isinstance(f, float))
    vk, nk = str('%.*f' % (dp, f)).split('.')
    return "%s,%s" % (fmtZahl(vk), str(nk))


def getRequest():
    return zope.security.management.getInteraction().participations[0]


def getPrincipal():
    return getRequest().principal
