# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import collections.abc

import uvcsite.browser
import uvcsite.browser.layout.slots.interfaces
import uvcsite.browser.layout.menu

from grokcore.component.interfaces import IContext
from grokcore.chameleon.components import ChameleonPageTemplateFile
from uvcsite import uvcsiteMF as _
from uvcsite.extranetmembership.interfaces import (
    IUserManagement, IExtranetMember)
from uvcsite.extranetmembership.vocabulary import vocab_berechtigungen
from uvcsite.interfaces import IHomeFolder, IHomeFolder
from zeam.form import base
from zope.component import getUtility
from zope.interface import Interface, directlyProvides
from zope.location import Location, LocationProxy
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.traversing.interfaces import ITraversable
from zope.interface import implementer
from zope.dublincore.interfaces import IDCDescriptiveProperties


grok.templatedir('templates')


class IOnTheFlyUser(IContext):
    pass


@implementer(IContext, IDCDescriptiveProperties)
class ENMSLister(Location):

    title = "Mitbenutzerverwaltung"

    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = "++%s++" % name
        self.um = getUtility(IUserManagement)
        self.mnr, self.az = self.um.zerlegUser(parent.__name__)
        self.user_schema = base.Fields(self.um.UserInterface)

    def delete(self, az):
        cn = '%s-%s' % (self.mnr, az)
        self.um.deleteUser(cn)
        for role in self.__parent__.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor', cn)

    def update(self, **data):
        cn = '%s-%s' % (self.mnr, data.get('az'))
        self.um.updUser(**data)
        for role in self.__parent__.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor', cn)
        for role in data.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.__parent__[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', cn)

    def get_users(self):
        for user in self.um.getUserGroups(self.mnr):
            directlyProvides(user, IOnTheFlyUser)
            yield LocationProxy(user, self, user['az'])

    def __iter__(self):
        return self.get_users()

    def __getitem__(self, az):
        user = None
        cn = '%s-%s' % (self.mnr, az)
        if self.um.getUser(cn):
            user = LocationProxy(self.um.getUser(cn), self, az)
            directlyProvides(user, IOnTheFlyUser)
        return user

    def get(self, az, default=None):
        return self[az] or default


@implementer(IContext)
class ENMSHomeFolderTraverser(grok.MultiAdapter):
    grok.context(IHomeFolder)
    grok.name('enms')
    grok.provides(ITraversable)
    grok.adapts(IHomeFolder, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        lister = ENMSLister(self.context, 'enms')
        if not name:
            return lister
        return lister.get(name)


class IndexRedirector(grok.View):
    grok.context(ENMSHomeFolderTraverser)
    grok.name('index')

    def render(self):
        self.redirect(self.url(self.context.context, '++enms++'))


class ENMSListerTraverser(grok.Traverser):
    grok.context(ENMSLister)

    def traverse(self, name):
        return self.context.get(name)


class ENMS(uvcsite.browser.Page):
    grok.name('index')
    grok.title('Mitbenutzerverwaltung')
    grok.context(ENMSLister)
    grok.require('uvc.ManageCoUsers')

    uniqueid = 'mnr'

    def user_fields(self, user):
        for field in self.fields:
            fieldname = field.identifier
            multi = False
            link = None
            if fieldname == 'rollen':
                value = user.get(fieldname, '')
                value = self.displayRoles(value)
            elif fieldname == self.uniqueid:
                value = '%s-%s' % (user['mnr'], user['az'])
                link = self.url(user)
            else:
                value = user.get(fieldname, '')
            if (isinstance(value, collections.abc.Iterable) and
                not isinstance(value, (str, bytes))):
                multi = True
            yield {'value': value, 'multi': multi, 'link': link}

    def update(self):
        self.fields = base.Fields(self.context.user_schema).omit(
            'passwort', 'confirm')
        self.users = iter(self.context)

    def displayRoles(self, roles):
        rc = []
        vb = vocab_berechtigungen(None)
        for role in roles:
            try:
                rc.append(vb.getTerm(role).title)
            except:
                pass
        return rc


class ENMSCreateUser(uvcsite.browser.Form):
    """ Simple Form which displays values from a Dict"""
    grok.context(ENMSLister)
    grok.require('uvc.ManageCoUsers')

    label = "Mitbenutzer anlegen"
    description = "Nutzen Sie diese Form um einen neuen Mitbenutzer anzulegen"

    ignoreContent = False

    mnr_template = ChameleonPageTemplateFile('templates/mnr.cpt')
    
    @property
    def fields(self):
        return base.Fields(self.context.user_schema)

    def updateForm(self):
        super(ENMSCreateUser, self).updateForm()
        self.fieldWidgets.get('form.field.mnr').template = self.mnr_template

    def getNextNumber(self, groups):
        all_azs = []
        for group in groups:
            all_azs.append(group['az'])
        if not all_azs:
            return 1
        return int(max(all_azs)) + 1

    def getDefaultData(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        all_users = self.getNextNumber(um.getUserGroups(principal))
        user = principal + '-' + str(all_users).zfill(2)
        rollen = [x for x in self.context.__parent__.keys()]
        print(rollen)
        return {'mnr': user, 'rollen': rollen}

    def update(self):
        data = self.getDefaultData()
        print (data)
        self.setContentData(base.DictDataManager(data))

    @base.action(_("Anlegen"))
    def anlegen(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        um = getUtility(IUserManagement)
        um.addUser(**data)
        # Setting Home Folder Rights
        for role in data.get('rollen'):
            principal_roles = IPrincipalRoleManager(
                self.context.__parent__[role])
            principal_roles.assignRoleToPrincipal(
                'uvc.Editor', data.get('mnr'))
        self.flash(_('Der Mitbenutzer wurde gespeichert'))
        principal = self.request.principal
        homeFolder = IHomeFolder(principal)
        self.redirect(self.url(homeFolder, '++enms++'))


class ENMSUpdateUser(uvcsite.browser.Form):
    """ A Form for updating a User in ENMS"""
    grok.name('index')
    grok.context(IOnTheFlyUser)
    grok.require('uvc.ManageCoUsers')

    ignoreContent = False
    label = "Mitbenutzer verwalten"
    description = ("Nutzen Sie diese Form um die Daten eines " +
                   "Mitbenutzers zu pflegen.")

    @property
    def fields(self):
        return base.Fields(self.context.__parent__.user_schema)

    def update(self):
        context = self.context
        context['confirm'] = context['passwort']
        self.setContentData(base.DictDataManager(context))

    def updateForm(self):
        super(ENMSUpdateUser, self).updateForm()
        mnr = self.fieldWidgets.get('form.field.mnr')
        pw = self.fieldWidgets.get('form.field.passwort')
        confirm = self.fieldWidgets.get('form.field.confirm')
        mnr.template = ChameleonPageTemplateFile('templates/mnr.cpt')
        pw.template = ChameleonPageTemplateFile('templates/password.cpt')
        confirm.template = ChameleonPageTemplateFile('templates/password.cpt')

    @base.action(_("Bearbeiten"))
    def anlegen(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        data['az'] = self.context['az']
        self.context.__parent__.update(**data)
        self.flash(_('Der Mitbenutzer wurde gespeichert'))
        self.redirect(self.url(self.context.__parent__))

    @base.action(_("Entfernen"))
    def entfernen(self):
        data, errors = self.extractData()
        self.context.__parent__.delete(self.context['az'])
        self.flash(_('Der Mitbenutzer wurde entfernt.'))
        self.redirect(self.url(self.context.__parent__))


class ChangePassword(uvcsite.browser.Form):
    """A Form for updating a User in ENMS.
    """
    grok.context(IHomeFolder)

    label = _('Passwort ändern')
    description = _('Hier können Sie Ihr Passwort ändern')
    # uvcsite.menu(uvcsite.PersonalMenu)
    grok.require('zope.View')
    ignoreContext = True

    fields = base.Fields(IExtranetMember).select('passwort', 'confirm')

    @base.action(_("Bearbeiten"))
    def changePasswort(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        um = getUtility(IUserManagement)
        principal = self.request.principal.id
        data['mnr'] = principal
        um.updatePasswort(**data)
        self.flash(_('Ihr Passwort wurde gespeichert!'))
        self.redirect(self.url(self.context))
