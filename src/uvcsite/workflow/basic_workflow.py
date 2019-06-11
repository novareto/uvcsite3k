# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvcsite.content.interfaces import IContent
from datetime import datetime

import uvcsite.workflow
from hurry.workflow import workflow
from hurry.workflow.interfaces import (
    IWorkflow, IWorkflowState, IWorkflowInfo, IWorkflowTransitionEvent)


def titleForState(state):
    """ Reverse Mapping of workflow States """
    mapping = {0: 'Entwurf', 1: 'gesendet', 2: 'in Verarbeitung', 3: 'Review'}
    return mapping.get(state, 'unbekannt')


def create_workflow():
    """ Basic Setup For Workflow Utility"""
    create_transition = workflow.Transition(
        transition_id='create',
        title='create',
        source=None,
        destination=uvcsite.workflow.State.CREATED)

    publish_transition = workflow.Transition(
        transition_id='publish',
        title='publish',
        source=uvcsite.workflow.State.CREATED,
        destination=uvcsite.workflow.State.PUBLISHED)

    progress_transition = workflow.Transition(
        transition_id='progress',
        title='progress',
        source=uvcsite.workflow.State.CREATED,
        destination=uvcsite.workflow.State.PROGRESS)

    fix_transition = workflow.Transition(
        transition_id='fix',
        title='fix',
        source=uvcsite.workflow.State.PROGRESS,
        destination=uvcsite.workflow.State.PUBLISHED)

    review = workflow.Transition(
        transition_id='review',
        title='publish_to_review',
        source=uvcsite.workflow.State.CREATED,
        destination=uvcsite.workflow.State.REVIEW)

    review_to_publish = workflow.Transition(
        transition_id='review_to_publish',
        title='review to publish',
        source=uvcsite.workflow.State.REVIEW,
        destination=uvcsite.workflow.State.PUBLISHED)

    return workflow.Workflow([create_transition,
                              progress_transition,
                              fix_transition,
                              review,
                              review_to_publish,
                              publish_transition])

grok.global_utility(create_workflow, provides=IWorkflow)


# Workflow States

class WorkflowState(workflow.WorkflowState, grok.Adapter):
    grok.context(IContent)
    grok.provides(IWorkflowState)


# Workflow Info

class WorkflowInfo(workflow.WorkflowInfo, grok.Adapter):
    grok.context(IContent)
    grok.provides(IWorkflowInfo)


# Events

@grok.subscribe(IContent, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
    IWorkflowInfo(content).fireTransition('create')


@grok.subscribe(IWorkflowTransitionEvent)
def set_publish_action(event):
    event.object.published = datetime.now()


# @grok.subscribe(IWorkflowTransitionEvent)
def change_permissions(event):
    if event.destination == PUBLISHED:
        obj = event.object
        principal = obj.principal
        from uvcsite.auth.interfaces import ICOUser
        from zope.securitypolicy import interfaces
        if not ICOUser.providedBy(uvcsite.getPrincipal()):
            prinper = interfaces.IPrincipalPermissionManager(obj)
            roleper = interfaces.IRolePermissionManager(obj)
            roleper.denyPermissionToRole('uvc.ViewContent', 'uvc.Editor')
            prinper.grantPermissionToPrincipal('uvc.ViewContent', principal.id)
