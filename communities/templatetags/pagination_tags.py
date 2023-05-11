from django import template
from django.core.paginator import Paginator

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate(context, object_list, per_page=10):
    paginator = Paginator(object_list, per_page)
    request = context['request']
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return ''
