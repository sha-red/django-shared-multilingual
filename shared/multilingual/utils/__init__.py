# Erik Stein <code@classlibrary.net>, 2017

from collections import OrderedDict
from django.conf import settings

from shared.utils.translation import lang_suffix


def i18n_fields(field_name, languages=None):
    return [lang_suffix(l, field_name) for l in languages or
        OrderedDict(settings.LANGUAGES).keys()]
