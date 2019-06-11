import martian
import uvcsite.content.interfaces

from zope.interface import classImplements
from zope.interface.interface import InterfaceClass
from zope.schema import getFieldsInOrder
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IField


class Fields:
    def __init__(self, *ifaces):
        fields = []
        for iface in ifaces:
            if isinstance(iface, InterfaceClass):
                for name, field in getFieldsInOrder(iface):
                    fields.append((name, field))
            elif IField.providedBy(iface):
                name = iface.__name__
                if not name:
                    raise ValueError(
                        "Field has no name")
                fields.append((name, iface))

        seq = []
        byname = {}
        for name, field in fields:
            name = field.__name__
            if name in byname:
                raise ValueError("Duplicate name", name)
            seq.append(field)
            byname[name] = field

        self.__Fields_seq__ = seq
        self.__Fields_byname__ = byname

    def __len__(self):
        return len(self.__Fields_seq__)

    def __iter__(self):
        return iter(self.__Fields_seq__)

    def __getitem__(self, name):
        return self.__Fields_byname__[name]

    def get(self, name, default=None):
        return self.__Fields_byname__.get(name, default)


def field_bootstrap(cls, *schemas):
    def fields_setter(inst, **kwargs):
        super(cls, inst).__init__(**kwargs)
        ifields = Fields(*schemas)
        for key, value in kwargs.items():
            ifield = ifields.get(key)
            if ifield is None:
                continue
            field = ifield.bind(inst)
            field.validate(value)
            field.set(inst, value)
    return fields_setter


def schema(*schemas):
    def schema_setter(cls):
        formfields = Fields(*schemas)
        for field in formfields:
            fname = field.__name__
            if not hasattr(cls, fname):
                setattr(cls, fname, FieldProperty(field))

        cls.__init__ = field_bootstrap(cls, *schemas)
        cls.__schema__ = schemas
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
