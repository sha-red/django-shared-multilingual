from functools import reduce, partial

from collections import OrderedDict
from django.conf import settings

from shared.utils.translation import get_language, lang_suffix


def i18n_fields(field_name, languages=None):
    """
    Returns a list of i18n fields for a given fieldname.
    >>> i18n_fields('title', ['en', 'de'])
    ['title_en', 'title_de']
    """
    return [lang_suffix(l, field_name) for l in languages or
        OrderedDict(settings.LANGUAGES).keys()]


def i18n_fields_list(field_names, languages=None):
    """
    Returns i18n fields for a list of fields, i.e.

    >>> search_fields = ['title', 'window_title', 'short_title']
    >>> i18n_fields_list(search_fields, ['en', 'de'])
    ['title_en', 'title_en', 'windowtitle_en', 'windowtitle_en', 'shorttitle_en', 'shorttitle_en', ]
    """
    f = partial(i18n_fields, languages=languages)
    return reduce(lambda x, y: x + y, map(f, field_names))
