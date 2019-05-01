from django import template
from django.db.models.functions import Lower
from django.db.models.query import QuerySet

from shared.utils.translation import lang_suffix


register = template.Library()


def orderable(field_name):
    return Lower(lang_suffix(fieldname=field_name))


@register.filter
def i18nsort(queryset, field_name):
    assert isinstance(queryset, QuerySet), "i18nsort only supports querysets."
    return queryset.order_by(orderable(field_name))
