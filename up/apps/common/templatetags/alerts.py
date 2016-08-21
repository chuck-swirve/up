"""
Reuse!
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django import template
from django.contrib import messages
from django.utils.html import format_html_join


ALERT_FMT = '''<div class="alert {} alert-dismissible">
  <button type="button" class="close" data-dismiss="alert"
          aria-label="Close">
    <span aria-hidden="true">
      &times;
    </span>
  </button>
  <span><strong>{}</strong> {}</span>
</div>
'''

register = template.Library()

@register.simple_tag
def render_form_errors(form):
    import pdb; pdb.set_trace()
    label_fmt = 'Error{}:'
    form_errors = []
    for field_name, errors in form.errors.items():
        field = form.fields.get(field_name)
        if field is None:
            label =  label_fmt.format('')
        else:
            label = label_fmt.format(' on "{}"'.format(field.label))
        for error in errors:
            form_errors.append(('alert-danger', label, unicode(error)))
    form_errors_html = format_html_join(
        '\n', ALERT_FMT,
        form_errors)
    return form_errors_html


@register.simple_tag(takes_context=True)
def render_messages(context):
    request = context.get('request')
    storage = messages.get_messages(request)
    messages_html = format_html_join(
        '\n', ALERT_FMT,
        ((message.level_tag, '', message) for message in storage)
    )
    return messages_html
