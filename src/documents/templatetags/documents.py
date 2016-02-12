# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.loader import get_template, select_template

from ..utils import stringify_value


register = template.Library()


HEADER_TPL = '<th id="column%s" data-sortby="%s">%s</th>'
TD_TPL = '<td class="column%s"><%%= %s %%></td>'


class MenuItem(object):
    def __init__(self, id, label, action, ajax=False, modal=None,
                 progression_modal=False, icon='', disabled=False):
        """Represents a single item in document actions menus.

        - id: the html id of the menu item.
        - label: the displayed text.
        - action: the action url.
        - ajax: should the action be submitted diretly or through an ajax request?
        - modal: the #id of the modal to display before submitting (if any)
        - progression_modal: should a progression bar be displayed?
        - icon: which glyphicon to display as the item icon?
        - disabled: is the menu item disabled?

        """
        self.id = id
        self.label = label
        self.action = action
        self.ajax = ajax
        self.modal = modal
        self.progression_modal = progression_modal
        self.icon = icon
        self.disabled = disabled

    def __unicode__(self):
        return self.to_html()

    def __str__(self):
        return self.to_html()

    def to_html(self):
        menu_entry = '''
            <li disabled="{disabled}">
            <a id="action-{id}"
                data-form-action="{action}"
                data-keyboard="false"
                data-ajax="{ajax}"
                data-modal="{modal}" >
                <span class="glyphicon glyphicon-{icon} glyphicon-white"></span>
                {label}
            </a>
            </li>
        '''.format(
            disabled='disabled' if self.disabled else '',
            id=self.id,
            action=self.action,
            ajax='true' if self.ajax else 'false',
            modal=self.modal or '',
            icon=self.icon,
            label=self.label
        )
        return menu_entry


@register.simple_tag()
def generate_header_markup(document_class):
    """Generates the markup to be used in doc list table header."""
    columns = document_class.PhaseConfig.column_fields

    headers = list()
    for column in columns:
        headers.append(HEADER_TPL % (
            column[1],
            column[1],
            column[0],
        ))

    return ' '.join(headers)


@register.simple_tag()
def generate_template_markup(document_class):
    """Generates the markup to be used in doc list table rows."""
    default_template = 'documents/columns/default.html'
    columns = document_class.PhaseConfig.column_fields

    tds = list()
    for column in columns:
        custom_template = 'documents/columns/{}.html'.format(column[1])
        tpl = select_template([custom_template, default_template])
        content = tpl.render({'field_name': column[1]})
        tds.append(content)

    return ' '.join(tds)


@register.filter
def stringify(val):
    return stringify_value(val)


# @register.simple_tag
# def action_menu(metadata, user):
#     actions = metadata.get_actions(user)
#     menu_items = map(action_menu_item, actions.items())
#     menu = '''
#     <ul class="dropdown-menu dropdown-menu-right">
#         <li>{}</li>
#     </ul>
#     '''.format('</li><li>'.join(menu_items))
#     return menu


@register.simple_tag()
def batch_action_menu(Metadata, category, user):
    actions = Metadata.get_batch_actions(category, user)
    menu = '''
    <ul class="dropdown-menu">
        {}
    </ul>
    '''.format(''.join(action.to_html() for action in actions.values()))
    return menu


@register.simple_tag(takes_context=True)
def include_batch_action_modals(context, Metadata):
    rendered = []
    for tpl in Metadata.get_batch_actions_modals():
        content = get_template(tpl)
        rendered.append(content.render(context))
    return '\n'.join(rendered)
