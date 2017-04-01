# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils import translation

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from xapian_backend import \
    XapianSearchBackend, XapianSearchQuery, XapianEngine


class MultilingualXapianSearchBackend(XapianSearchBackend):
    def update(self, index, iterable, commit=True, language_specific=False):
        if not language_specific and self.connection_alias == "default":
            current_language = (translation.get_language() or settings.LANGUAGE_CODE)[:2]
            for lang_code, lang_name in settings.LANGUAGES:
                using = "default_%s" % lang_code
                translation.activate(lang_code)
                backend = connections[using].get_backend()
                backend.update(index, iterable, commit,
                    language_specific=True)
            translation.activate(current_language)
        elif language_specific:
            super(MultilingualXapianSearchBackend, self).\
                update(index, iterable, commit)


class MultilingualXapianSearchQuery(XapianSearchQuery):
    def __init__(self, using=DEFAULT_ALIAS):
        lang_code = translation.get_language()[:2]
        using = "default_%s" % lang_code
        super(MultilingualXapianSearchQuery, self).__init__(using)


class MultilingualXapianEngine(XapianEngine):
    backend = MultilingualXapianSearchBackend
    query = MultilingualXapianSearchQuery
