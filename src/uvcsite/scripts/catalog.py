import transaction
import zope.app.wsgi
import zope.app.debug
import zope.component.hooks
import zope.component
import zope.catalog
from zope.intid.interfaces import IIntIds


def recatalog_app(app, items_iterator, size=3000):
    zope.component.hooks.setSite(app)
    ids = zope.component.getUtility(IIntIds)
    catalogs = list(
        zope.component.getUtilitiesFor(zope.catalog.interfaces.ICatalog))
    counter = 0
    with transaction.manager as tr:
        for obj in items_iterator(app):
            counter += 1
            for name, catalog in catalogs:
                id = ids.queryId(obj)
                if id is not None:
                    catalog.index_doc(id, obj)
            if not counter % size:
                tr.commit()
    zope.component.hooks.setSite()


def global_recataloging(zope_conf):
    db = zope.app.wsgi.config(zope_conf)
    debugger = zope.app.debug.Debugger.fromDatabase(db)
    root = debugger.root()
    for app in root.values():
        recatalog_app(app, None)
