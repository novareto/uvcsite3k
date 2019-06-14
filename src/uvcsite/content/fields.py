from zope.interface.interface import InterfaceClass
from zope.schema import getFieldsInOrder
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
