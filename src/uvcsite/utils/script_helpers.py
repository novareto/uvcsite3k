# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


from zope.publisher.browser import TestRequest
from hurry.workflow.interfaces import IWorkflowState


def getContentInAllFolders(homefolderbase, wf_status=None):
    for homefolder in homefolderbase._SampleContainer__data.itervalues():
        for productfolder in homefolder._SampleContainer__data.itervalues():
            for content in productfolder._SampleContainer__data.itervalues():
                if wf_status is not None:
                    if IWorkflowState(content).getState() == wf_status:
                        yield content
                else:
                    yield content


class FakeEvent(object):

    def __init__(self, principal):
        self.principal = principal
        self.request = TestRequest()


class FakeFactory(object):

    def __init__(self, principal):
        self.principal = principal


def getEvent(content):
    return FakeEvent(content.principal)
