import grok
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getSiteManager
from zope.intid.interfaces import IIntIds
from zope.authentication.interfaces import IAuthentication
from zope.cachedescriptors.property import CachedProperty
from zope.pluggableauth.interfaces import (
    IAuthenticatorPlugin, ICredentialsPlugin)
import uvcsite.plugins


class Cataloger:

    def __init__(self, catalog, trigger):
        self.catalog = catalog  # grok.Indexes class
        self.trigger = trigger  # Event class

    @CachedProperty
    def title(self):
        catalog_name = grok.name.bind().get(self.catalog)
        return 'Cataloger: %s' % catalog_name

    @property
    def status(self):
        catalog_name = grok.name.bind().get(self.catalog)
        catalog = queryUtility(ICatalog, name=catalog_name) is not None
        if catalog:
            return uvcsite.plugins.Status(
                state=uvcsite.plugins.States.INSTALLED
            )
        return uvcsite.plugins.Status(
            state=uvcsite.plugins.States.NOT_INSTALLED
        )

    def get(self, site):
        sm = site.getSiteManager()
        name = grok.name.bind().get(self.catalog)
        return sm.queryUtility(ICatalog, name=name)

    def install(self, site):
        try:
            grok.notify(self.trigger(site))
        except:
            # should log
            pass
        if self.get(site) is None:
            raise uvcsite.plugins.PluginError(
                self.title,
                u'Catalog registration was unsuccessful.')

    def uninstall(self, site):
        sm = site.getSiteManager()
        catalog_name = grok.name.bind().get(self.catalog)
        catalog = sm.queryUtility(ICatalog, name=catalog_name)
        if catalog is not None:
            sm.unregisterUtility(
                catalog, provided=ICatalog, name=catalog_name)
            del sm[catalog.__name__]

    def recatalog(self, site, items_iterator):
        sm = site.getSiteManager()
        catalog_name = grok.name.bind().get(self.catalog)
        catalog = sm.getUtility(ICatalog, name=catalog_name)
        ids = sm.getUtility(IIntIds)

        counter = 0
        for obj in items_iterator:
            id = ids.queryId(obj)
            if id is not None:
                catalog.index_doc(id, obj)
                counter += 1

        return counter

    def diagnose(self, site):
        sm = site.getSiteManager()
        catalog_name = grok.name.bind().get(self.catalog)
        catalog = sm.getUtility(ICatalog, name=catalog_name)
        indexes = list(catalog.keys())
        return {
            'Plugin': self.title,
            'Indexes': ', '.join(indexes),
            'Catalog name': catalog_name,
            'Number of documents': catalog[indexes[0]].documentCount(),
        }


class PAUComponent:

    types = {
        'authenticator': (
            'authenticatorPlugins', IAuthenticatorPlugin),
        'credentials': (
            'credentialsPlugins', ICredentialsPlugin)
    }

    def __init__(self, component, type):
        self.component = component  # callable factory
        assert type in self.types
        self.type = type
        self.attribute, self.provides = self.types[type]

    @CachedProperty
    def title(self):
        return 'PAUComponent: %s (%s)' % (self.component.__name__, self.type)

    @property
    def status(self):
        pau = queryUtility(IAuthentication)
        name = grok.name.bind().get(self.component)
        pau_available = name in getattr(pau, self.attribute)

        sm = getSiteManager()
        sm_available = name in sm

        if pau_available and sm_available:
            return uvcsite.plugins.Status(
                state=uvcsite.plugins.States.INSTALLED)

        if pau_available or sm_available:
            return uvcsite.plugins.Status(
                state=uvcsite.plugins.States.INCONSISTANT)

        return uvcsite.plugins.Status(
            state=uvcsite.plugins.States.NOT_INSTALLED)

    def get(self, site):
        sm = site.getSiteManager()
        name = grok.name.bind().get(self.component)
        return sm.queryUtility(self.provides, name=name)

    def install(self, site):
        sm = site.getSiteManager()
        pau = sm.queryUtility(IAuthentication)
        name = grok.name.bind().get(self.component)

        values = getattr(pau, self.attribute)
        if name not in values:
            setattr(pau, self.attribute, values + (name,))

        if name not in sm:
            sm = site.getSiteManager()
            utility = self.component()
            sm[name] = utility
            sm.registerUtility(
                utility, provided=IAuthenticatorPlugin, name=name)
        return True

    def uninstall(self, site):
        sm = site.getSiteManager()
        pau = sm.queryUtility(IAuthentication)
        name = grok.name.bind().get(self.component)

        if name in sm:
            sm = site.getSiteManager()
            utility = sm[name]
            sm.unregisterUtility(
                utility, provided=IAuthenticatorPlugin, name=name)
            del sm[name]

        values = getattr(pau, self.attribute)
        setattr(pau, self.attribute, tuple((p for p in values if p != name)))
        return True
