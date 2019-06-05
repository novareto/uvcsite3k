import sys
import grok
import zope.interface
import zope.component

from collections import namedtuple
from functools import wraps

from zeam.form.base import Errors, Error, Actions, Action, FAILURE
from zope.location import LocationProxy
from zope.publisher.interfaces import browser
from zope.traversing.interfaces import ITraversable
from zope.dublincore.interfaces import IDCDescriptiveProperties

import uvcsite.plugins
from uvcsite.plugins import flags


class Status:

    def __init__(self, state, *infos):
        assert state in flags.States
        self.state = state
        self.infos = infos

    def __str__(self):
        return str(self.state.value)

    def __repr__(self):
        '<Status %s>' % self.state.value


class Result:

    def __init__(self, type, value, redirect=False):
        assert type in flags.ResultTypes
        self.type = type
        self.value = value
        self.redirect = redirect
        
    def __str__(self):
        return str(self.type.value)

    def __repr__(self):
        '<Result %s>' % self.type.value


class PluginError(Exception):

    def __init__(self, title, *messages):
        Exception.__init__(self, title)
        self.messages = messages


class IPlugin(zope.interface.Interface):

    title = zope.interface.Attribute('Title')
    description = zope.interface.Attribute('Description')
    actions = zope.interface.Attribute('Actions')
    status = zope.interface.Attribute('Plugin status')


class IComplexPlugin(IPlugin):

    subplugins = zope.interface.Attribute('Subplugins')


class PluginAction(Action):

    prefix = "plugin"

    def __init__(self, callback, title, states):
        self.states = states
        self.callback = callback
        Action.__init__(
            self, title=title, identifier=callback.__name__)

    def available(self, form):
        plugin = form.getContent()
        return plugin.status.state in self.states

    def __call__(self, form):
        site = grok.getApplication()
        content = form.getContent()
        try:
            result = self.callback(content, site)
            assert isinstance(result, Result)
            return result
        except PluginError as exc:
            form.errors = Errors(*[
                Error(title=error, identifier=self.identifier)
                for error in exc.messages])
        return FAILURE


def plugin_action(title, *valid_states):
    if not valid_states:
        valid_states = flags.States
    def callback(method):
        frame = sys._getframe(1)
        f_locals = frame.f_locals
        actions = f_locals.setdefault('actions', Actions())
        action = PluginAction(method, title, valid_states)
        actions.append(action)
        return method
    return callback


@zope.interface.implementer(IDCDescriptiveProperties, IPlugin)
class Plugin(grok.GlobalUtility):
    grok.baseclass()
    grok.provides(IPlugin)

    title = None
    description = u""
    status = Status(state=flags.States.NOT_INSTALLED)
    actions = None


@zope.interface.implementer(IComplexPlugin)
class ComplexPlugin(Plugin):
    grok.baseclass()

    subplugins = None  # dict

    def dispatch(self, action, site):
        errors = []
        for sp in self.subplugins.values():
            try:
                method = getattr(sp, action, None)
                if method is not None:
                    result = method(site)
            except uvcsite.plugins.PluginError as exc:
                errors.extend(exc.messages)

        if errors:
            raise uvcsite.plugins.PluginError(
                u'`%s` encountered errors.' % action, *errors)

        return uvcsite.plugins.Result(
            value=u'`%s` was successful.' % action,
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @property
    def status(self):
        statuses = [sp.status for sp in self.subplugins.values()]
        states = set((s.state for s in statuses))
        if len(states) > 1:
            status = uvcsite.plugins.Status(
                state=flags.States.INCONSISTANT)
        elif flags.States.INSTALLED in states:
            status = uvcsite.plugins.Status(
                state=flags.States.INSTALLED)
        else:
            status = uvcsite.plugins.Status(
                state=flags.States.NOT_INSTALLED)

        for s in statuses:
            if s.infos:
                status.infos.extend(s.infos)

        return status
