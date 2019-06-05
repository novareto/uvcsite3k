# -*- coding: utf-8 -*-

from uvcsite import uvcsiteMF as _
from zope.interface import Interface, invariant, Invalid
from zope.schema import Password, TextLine, Choice, Set
from uvcsite.extranetmembership.vocabulary import vocab_berechtigungen


class IExtranetMember(Interface):

    mnr = TextLine(
        title=_(u"Mitgliedsnummer"),
        description=_(
            u"Benutzername für den Mitbenutzer (Mitgliedsnummer-lfd.Nr.)"),
        required=True)

    rollen = Set(
        title=_(u"Berechtigung"),
        description=_(u"Berechtigung"),
        value_type=Choice(source=vocab_berechtigungen),
        required=False)

    passwort = Password(
        title=_(u"Passwort"),
        description=_(u"Bitte tragen Sie hier das Passwort ein."),
        min_length=5,
        max_length=8,
        required=True)

    confirm = Password(
        title=_(u"Bestätigung"),
        description=_(u"Bitte bestätigen Sie das eingegebene Passwort."),
        min_length=5,
        max_length=8,
        required=True)

    @invariant
    def arePasswordsEqual(user):
        if user.passwort != user.confirm:
            raise Invalid(
                u"Das Passwort und die Wiederholung sind nicht gleich.")

    def getBaseUser():
        """Return the User Representation
        """


class IUserManagement(Interface):

    def getUser(mnr):
        """Return the specified User
        """

    def getUserGroup(mnr):
        """Return a group of a User from a company
        """

    def addUser(**kw):
        """Add a User to store
        """

    def updateUser(mnr, **kw):
        """Update a specified user
        """

    def deleteUser(mnr):
        """Delete a specified user
        """

    def updatePasswort(**kw):
        """Change a Users Passwort
        """
