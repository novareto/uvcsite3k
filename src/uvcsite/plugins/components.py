import sys
import grok
import zope.interface
import zope.component
import collections

from zeam.form.base import Errors, Error, Action, FAILURE
from zope.dublincore.interfaces import IDCDescriptiveProperties

import uvcsite.plugins
from uvcsite.plugins import flags


class Status:

    def __init__(self, state, *infos):
        self.state = flags.States(state)
        self.infos = infos

    def __str__(self):
        return str(self.state.value)

    def __repr__(self):
        return f'<Status "{self.state.value}">'

    def __eq__(self, other):
        return (other.__class__ == self.__class__ and
                other.state == self.state and self.infos == other.infos)

class Result:

    def __init__(self, type, value, redirect=False):
        self.type = flags.ResultTypes(type)
        self.value = value
        self.redirect = redirect

    def __str__(self):
        return str(self.type.value)

    def __repr__(self):
        return f'<Result "{self.type.value}" redirect={self.redirect}>'

    def __eq__(self, other):
        return ((other.__class__ == self.__class__ and
                 other.type == self.type and
                 self.value == other.value and
                 self.redirect == other.redirect))


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


def plugin_action(title, *valid_states):
    if not valid_states:
        valid_states = flags.States

    def callback(method):
        frame = sys._getframe(1)
        f_locals = frame.f_locals
        actions = f_locals.setdefault('actions', collections.OrderedDict())
        actions[title] = (method, valid_states)
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

    subplugins = None  # tuple

    def dispatch(self, action, site):
        errors = []
        for sp in self.subplugins:
            try:
                method = getattr(sp, action, None)
                if method is not None:
                    _ = method(site)
            except PluginError as exc:
                errors.extend(exc.messages)

        if errors:
            raise PluginError(f'`{action}` encountered errors.', *errors)

        return Result(
            value=u'`%s` was successful.' % action,
            type=flags.ResultTypes.MESSAGE,
            redirect=True)

    @property
    def status(self):
        statuses = [sp.status for sp in self.subplugins]
        states = set((s.state for s in statuses))
        if len(states) > 1:
            status = Status(state=flags.States.INCONSISTANT)
        elif flags.States.INSTALLED in states:
            status = Status(state=flags.States.INSTALLED)
        else:
            status = Status(state=flags.States.NOT_INSTALLED)

        for s in statuses:
            if s.infos:
                status.infos.extend(s.infos)

        return status
