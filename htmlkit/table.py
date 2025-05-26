from markupsafe import Markup
from markupsafe import escape

class Column:

    def __init__(
        self,
        attrname,
        label = None,
        th_attrs = None,
        td_attrs = None,
        formatter = None,
    ):
        self.attrname = attrname
        self.label = label
        self.th_attrs = th_attrs
        self.td_attrs = td_attrs
        self.formatter = formatter

    def __html__(self):
        return self.label or self.attrname

    def render(self, instance):
        value = getattr(instance, self.attrname)
        formatter = self.formatter
        if callable(formatter):
            value = formatter(value)
        return Markup(value)

    def render_th(self):
        return f'<th{render_attrs(self.th_attrs)}>{Markup(self)}</th>'

    def render_td(self, instance):
        return f'<td{render_attrs(self.td_attrs)}>{self.render(instance)}</td>'


class Table:

    def __init__(self, columns, table_attrs=None):
        self.columns = columns
        self.table_attrs = table_attrs

    def render(self, instances):
        html = [f'<thead>']

        html.append('<tr>')
        for column in self.columns:
            html.append(column.render_th())
        html.append('</tr>')
        html.append('</thead>')

        html.append('<tbody>')
        for obj in instances:
            html.append('<tr>')
            for column in self.columns:
                html.append(column.render_td(obj))
            html.append('</tr>')
        html.append('</tbody>')
        return Markup(''.join(html))


def render_attrs(attrs):
    """
    Render dict of attributes for an html element as a string.
    """
    if attrs:
        attr_string = ' '.join(f'{key}="{escape(val)}"' for key, val in attrs.items())
        if attr_string:
            return ' ' + attr_string

    return ''
