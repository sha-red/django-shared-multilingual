from collections import OrderedDict
from functools import reduce, partial

from django.conf import settings

from shared.utils.translation import lang_suffix


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


def i18n_mainlang(field_name):
    """
    Returns the field name with the language code for the
    setting's main language appended.
    """
    return lang_suffix(settings.LANGUAGE_CODE, field_name=field_name)


# TODO Not functional
# def i18n_ordering(*field_list):
#     def dynamic_i18n_ordering(*args, **kwargs):
#         lang = get_language()
#         return [lang_suffix(lang, f) for f in field_list]
#     return dynamic_i18n_ordering

