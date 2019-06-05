# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


from zeam.form.base.markers import NO_VALUE, NO_CHANGE
from zeam.form.base.interfaces import IDataManager
from zeam.form.base.datamanager import ObjectDataManager


def set_fields_data(fields, content, data):
    """Applies the values to the fields, if a change has been made and
    if the field is present in the given fields manager. It returns a
    dictionnary describing the changes applied with the name of the field
    and the interface from where it's from.
    """
    changes = {}
    if not IDataManager.providedBy(content):
        content = ObjectDataManager(content)

    for identifier, value in data.items():
        field = fields.get(identifier, default=None)
        if (field is None or value is NO_VALUE or
            value is NO_CHANGE or field.isEmpty(value)):
            continue

        content.set(identifier, value)
        changes.setdefault(field.interface, []).append(identifier)

    return changes
