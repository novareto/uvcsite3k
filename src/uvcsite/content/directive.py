import martian
import uvcsite.content.interfaces
import uvcsite.content.fields
from zope.schema.fieldproperty import FieldProperty


def schema(*schemas):
    def schema_setter(cls):
        assert uvcsite.content.interfaces.IContent.implementedBy(cls)
        formfields = uvcsite.content.fields.Fields(*schemas)
        for field in formfields:
            fname = field.__name__
            if not hasattr(cls, fname):
                setattr(cls, fname, FieldProperty(field))

        cls.schema = schemas
        return cls
    return schema_setter


class contenttype(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = None
    validate = martian.validateClass


class productfolder(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = None
    validate = martian.validateText
