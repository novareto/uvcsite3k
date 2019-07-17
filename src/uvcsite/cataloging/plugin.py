import grok
import uvcsite
import uvcsite.cataloging
import uvcsite.plugins

from collections import defaultdict
from zope.component.hooks import getSite


CATALOG_DOC = u"""Write me

This is a documentation about...
"""


def getMembersContents(site):
    members = site.get('members')
    if members is not None:
        for homefolder in members:
            for productfolder in homefolder:
                for content in productfolder:
                    yield content


class CatalogPlugin(uvcsite.plugins.subplugins.Cataloger,
                    uvcsite.plugins.components.Plugin):
    grok.name('uvcsite.catalog')

    fa_icon = 'book'
    title = u"Generic catalog"
    description = "Cataloging capabilities for efficient lookups and sorting"

    def __init__(self):
        self.catalog = uvcsite.cataloging.catalogs.WorkflowCatalog
        self.trigger = uvcsite.cataloging.events.CatalogDeployment

    @uvcsite.plugins.components.plugin_action('Documentation')
    def documentation(self, site):
        return uvcsite.plugins.components.Result(
            value=CATALOG_DOC,
            type=uvcsite.plugins.flags.ResultTypes.PLAIN)

    @uvcsite.plugins.components.plugin_action(
        'Install', uvcsite.plugins.flags.States.NOT_INSTALLED)
    def _install(self, site):
        super(CatalogPlugin, self).install(site)
        return uvcsite.plugins.components.Result(
            value=u'Install was successful.',
            type=uvcsite.plugins.flags.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.components.plugin_action(
        'Diagnostic', uvcsite.plugins.flags.States.INSTALLED)
    def _diagnose(self, site):
        diag = super(CatalogPlugin, self).diagnose(site)
        return uvcsite.plugins.components.Result(
            value=diag,
            type=uvcsite.plugins.flags.ResultTypes.JSON)

    @uvcsite.plugins.components.plugin_action(
        'Recatalog', uvcsite.plugins.flags.States.INSTALLED)
    def _recatalog(self, site):
        super(CatalogPlugin, self).recatalog(site, getMembersContents(site))
        return uvcsite.plugins.components.Result(
            value=u'Recataloging was successful.',
            type=uvcsite.plugins.flags.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.components.plugin_action(
        'Uninstall', uvcsite.plugins.flags.States.INSTALLED)
    def _uninstall(self, site):
        super(CatalogPlugin, self).uninstall(site)
        return uvcsite.plugins.components.Result(
            value=u'Uninstall was successful.',
            type=uvcsite.plugins.flags.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.components.plugin_action(
        'Count', uvcsite.plugins.flags.States.INSTALLED)
    def count(self, site):
        catalog = self.get(site)
        counted = defaultdict(dict)
        for type, tids in catalog['type']._fwd_index.items():
            for state, sids in catalog['state']._fwd_index.items():
                counted[type][state] = len(set(tids) & set(sids))
        return uvcsite.plugins.components.Result(
            value=counted,
            type=uvcsite.plugins.flags.ResultTypes.JSON)
