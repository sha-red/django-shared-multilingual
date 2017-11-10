# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import string_concat

from shared.utils.translation import get_language, lang_suffix


class TranslatableCharField(models.CharField):

    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super(TranslatableCharField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            localized_field = models.CharField(
                string_concat(self.verbose_name, " (%s)" % lang_code),
                name=self.name,
                primary_key=self.primary_key,
                max_length=self.max_length,
                unique=self.unique,
                blank=_blank,
                null=False,  # intentionally ignored
                db_index=self.db_index,
                rel=self.rel,
                default=self.default or "",
                editable=self._editable,
                serialize=self.serialize,
                choices=self.choices,
                help_text=self.help_text,
                db_column=None,
                db_tablespace=self.db_tablespace
            )

            localized_field.contribute_to_class(
                cls,
                "%s%s" % (name, lang_suffix(lang_code)),
            )

        def translated_value(self):
            # For empty / non-existing translation fall back to main field
            language = get_language()
            val = self.__dict__["%s%s" % (name, lang_suffix(language))]
            if not val:
                val = self.__dict__["%s%s" % (name, lang_suffix(settings.LANGUAGE_CODE))]
            return val

        setattr(cls, name, property(translated_value))


class TranslatableTextField(models.TextField):

    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super(TranslatableTextField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            localized_field = models.TextField(
                string_concat(self.verbose_name, " (%s)" % lang_code),
                name=self.name,
                primary_key=self.primary_key,
                max_length=self.max_length,
                unique=self.unique,
                blank=_blank,
                null=False,  # intentionally ignored
                db_index=self.db_index,
                rel=self.rel,
                default=self.default or "",
                editable=self._editable,
                serialize=self.serialize,
                choices=self.choices,
                help_text=self.help_text,
                db_column=None,
                db_tablespace=self.db_tablespace
            )

            localized_field.contribute_to_class(
                cls,
                "%s%s" % (name, lang_suffix(lang_code)),
            )

        def translated_value(self):
            language = get_language()
            val = self.__dict__["%s%s" % (name, lang_suffix(language))]
            if not val:
                val = self.__dict__["%s%s" % (name, lang_suffix(settings.LANGUAGE_CODE))]
            return val

        setattr(cls, name, property(translated_value))


class TranslatableJSONField(JSONField):

    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super().__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        print(self, cls)
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            localized_field = JSONField(
                string_concat(self.verbose_name, " (%s)" % lang_code),
                name=self.name,
                primary_key=self.primary_key,
                max_length=self.max_length,
                unique=self.unique,
                blank=_blank,
                null=False,  # intentionally ignored
                db_index=self.db_index,
                rel=self.rel,
                default=self.default or "",
                editable=self._editable,
                serialize=self.serialize,
                choices=self.choices,
                help_text=self.help_text,
                db_column=None,
                db_tablespace=self.db_tablespace,
                encoder=self.encoder
            )

            localized_field.contribute_to_class(
                cls,
                "%s%s" % (name, lang_suffix(lang_code)),
            )

        def translated_value(self):
            language = get_language()
            val = self.__dict__["%s%s" % (name, lang_suffix(language))]
            if not val:
                val = self.__dict__["%s%s" % (name, lang_suffix(settings.LANGUAGE_CODE))]
            return val

        setattr(cls, name, property(translated_value))
