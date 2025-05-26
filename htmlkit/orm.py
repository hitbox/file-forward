from sqlalchemy import inspect

from .table import Column
from .table import Table

def has_info_label(obj):
    return (
        hasattr(obj, 'info')
        and isinstance(obj.info, dict)
        and obj.info
        and 'label' in obj.info
    )

def create_column(model, attrname, column_class=Column):
    mapper = inspect(model)
    attr = getattr(model, attrname)

    info = getattr(attr, 'info', {})
    label = info.get('label')
    th_attrs = info.get('th_attrs')
    td_attrs = info.get('td_attrs')
    column = Column(
        attrname,
        label = label,
        th_attrs = th_attrs,
        td_attrs = td_attrs,
    )
    return column

def example_get_attrs():
    attrs = []
    for name in dir(model):
        attr = getattr(model, name)
        if name in mapper.column_attrs:
            column_property = mapper.column_attrs[name]
            if column_property in mapper.primary_key:
                continue
            attrs.append(name)

def model_table(
    model,
    table_class = Table,
    column_class = Column,
):
    """
    Convert database model to html table object.
    """
    mapper = inspect(model)
    ui_meta = getattr(model, '__ui_meta__', {})
    columns = []
    for attrname, opts in ui_meta.items():
        attr_meta = ui_meta.get(attrname, {})
        column = column_class(
            attrname = attrname,
            label = attr_meta.get('label'),
            th_attrs = attr_meta.get('th_attrs'),
            td_attrs = attr_meta.get('td_attrs'),
            formatter = attr_meta.get('formatter'),
        )
        columns.append(column)

    table = table_class(columns)
    return table
