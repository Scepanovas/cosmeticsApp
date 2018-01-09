from django import template
import sys

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        if pattern == '/profilis/':
            if pattern != request.path:
                return ''
        if len(pattern) == 1 &  len(pattern) != len(request.path):
            return ''
        return 'active'
    return ''

    """
<WSGIRequest: GET '/'>
/ingredientai/ """
