import grok
import uvcsite.browser
import uvcsite.utils.forms
import uvcsite.content.interfaces
import uvcsite.content.tables
import uvcsite.browser
import uvcsite.browser.forms
import uvcsite.browser.layout.slots.interfaces

from megrok.pagetemplate import PageTemplate
from megrok.z3ctable import Values
from uvcsite import uvcsiteMF as _
from zeam.form import base
from zeam.form.base import Fields
from zeam.form.base.interfaces import ISimpleForm
from zope.component import getMultiAdapter
from zope.interface import Interface, implementer
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir('templates')


@implementer(uvcsite.content.tables.IContainerTable)
class Index(uvcsite.browser.TablePage):
    grok.name('index')
    grok.context(uvcsite.content.interfaces.IProductFolder)
    grok.require('uvc.ViewContent')

    description = u"Hier finden Sie alle Dokumente dazu."
    cssClasses = {'table': ('tablesorter table table-striped '
                            + 'table-bordered table-condensed')}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    sortOnId = "table-modified-5"
    sortOn = "table-modified-5"

    @property
    def title(self):
        return self.context.getContentName()

    def update(self):
        items = self.request.form.get('table-checkBox-0-selectedItems')
        if items and 'form.button.delete' in self.request:
            if isinstance(items, (str, unicode)):
                items = [items]
            for key in items:
                if key in self.context:
                    self.executeDelete(self.context[key])
        super().update()

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def getAddLinkUrl(self):
        url = grok.url(self.request, self.context)
        return f"{url}/@@add"

    def getAddTitle(self):
        return self.context.title

    def renderCell(self, item, column, colspan=0):
        from z3c.table import interfaces
        if interfaces.INoneCell.providedBy(column):
            return u''
        cssClass = column.cssClasses.get('td')
        cssClass = self.getCSSHighlightClass(column, item, cssClass)
        cssClass = self.getCSSSortClass(column, cssClass)
        cssClass = self.getCSSClass('td', cssClass)
        colspanStr = colspan and ' colspan="%s"' % colspan or ''
        dt = ' data-title="%s" ' % column.header
        return u'\n      <td%s%s%s>%s</td>' % (
            cssClass, colspanStr, dt, column.renderCell(item))


class ProductFolderValues(Values):
    """This Adapter returns IContent Objects
       form child folders
    """
    grok.adapts(uvcsite.content.interfaces.IProductFolder, None, Index)

    @property
    def values(self):
        results = []
        interaction = self.request.interaction
        for value in self.context.values():
            if interaction.checkPermission('uvc.ViewContent', value):
                results.append(value)
        return results


class ExtraViewsViewlet(grok.ViewletManager):
    grok.order(20)
    grok.baseclass()
    grok.view(Interface)
    grok.name('extra-views')
    grok.viewletmanager(uvcsite.browser.layout.slots.interfaces.IAboveContent)
    grok.require("zope.Public")

    # menu_factory = menus.ExtraViews
    menu_factory = object()

    def update(self):
        super().update()
        if not len(self.menu.viewlets) or ISimpleForm.providedBy(self.view):
            self.actions = None
        else:
            self.actions = self.compute_actions(self.menu.viewlets)

    def compute_actions(self, viewlets):
        for action in viewlets:
            selected = action.viewName == self.view.__name__
            context_url = self.menu.view.url(self.menu.context)
            url = selected and None or "%s/%s" % (context_url, action.viewName)
            yield {
                'id': action.__name__,
                'url': url,
                'title': action.title or action.__name__,
                'selected': selected,
                'class': (selected and 'selected ' +
                          self.menu.menu_class or self.menu.menu_class),
                }


class AddMenuViewlet(grok.Viewlet):
    grok.view(Index)
    grok.order(30)
    grok.context(uvcsite.content.interfaces.IProductFolder)
    grok.viewletmanager(uvcsite.browser.layout.slots.interfaces.ITabs)

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class AddMenu(PageTemplate):
    grok.view(AddMenuViewlet)


class Add(uvcsite.browser.forms.AddForm):
    grok.context(uvcsite.content.interfaces.IProductFolder)
    grok.require('uvc.AddContent')

    @property
    def label(self):
        return self.context.title

    description = u"Bitte füllen Sie die Eingabeform."

    @property
    def fields(self):
        content_object = self.context.getContentType()
        return Fields(*content_object.schema)

    def create(self, data):
        content = self.context.getContentType()()
        uvcsite.utils.forms.set_fields_data(self.fields, content, data)
        return content

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        self.flash(_('Added Content'))
        return self.url(self.context)


class Edit(uvcsite.browser.Form):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.require('uvc.EditContent')
    ignoreContent = False

    @property
    def fields(self):
        return Fields(*self.context.schema)

    @base.action(u'Speichern')
    def handle_apply(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type="error")
            return
        changes = uvcsite.browser.forms.apply_data_event(self.fields, self.context, data)
        if changes:
            self.flash(u'Ihre Daten wurden erfolgreich gendert', type="info")
            return
        else:
            self.flash('Kein Änderung', type="info")


class Display(uvcsite.browser.Form):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.name('index')
    grok.require('uvc.ViewContent')

    mode = base.DISPLAY
    ignoreContent = False

    @property
    def fields(self):
        return Fields(*self.context.schema)
