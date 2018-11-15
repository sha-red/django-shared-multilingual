# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import NOT_PROVIDED
from django.utils.text import format_lazy

from shared.utils.translation import get_language, lang_suffix


def get_translated_value(fieldname):
    def translated_value(obj):
        language = get_language()
        val = obj.__dict__[lang_suffix(language, fieldname)]
        if not val:
            other_languages = list(dict(settings.LANGUAGES).keys())
            other_languages.remove(language)
            for lang in other_languages:
                val = obj.__dict__[lang_suffix(lang, fieldname)]
                if val:
                    break
        return val
    return translated_value


class TranslatableFieldMixin:
    """
    Make a Field subclass translatable, i.e. it automatically provides field duplicates
    for each language defined in settings.LANGUAGES.

    Parameters:
        base_class
            optional, is None first base class which is a subclass of Django's Field class is used
        extra_parameter_names
            optional, attributes of the original field to be copied to the localized fields

    Usage:

        class TranslatableRichTextField(TranslatableFieldMixin, RichTextField):
            base_class = RichTextField
            extra_parameter_names = ['config_name', 'extra_plugins', 'external_plugin_resources']
    """

    base_class = None
    formfield_class = forms.fields.CharField
    extra_parameter_names = []

    def __init__(self, verbose_name=None, **kwargs):
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super().__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            params = {
                'blank': _blank,
                'choices': self.choices,
                'db_column': None,
                'db_index': self.db_index,
                'db_tablespace': self.db_tablespace,
                'default': self.default,
                'editable': self._editable,
                'help_text': self.help_text,
                'max_length': self.max_length,
                'name': self.name,
                'null': False,  # intentionally ignored
                'primary_key': self.primary_key,
                'rel': self.remote_field,
                'serialize': self.serialize,
                'unique': self.unique,
            }

            # TODO If null=False/blank=False add validator which checks that at
            #      least one field has a value

            # Because we never allow NULL set empty string as default
            if params['default'] == NOT_PROVIDED:
                params['default'] = ''

            for n in self.extra_parameter_names:
                params[n] = getattr(self, n, None)

            if self.db_column:
                params['db_column'] = lang_suffix(lang_code, self.db_column)

            # TODO Move this logic to a meta class?
            if not self.base_class:
                # Get first base class which is a subclass of Django's Field
                self.base_class = [f for f in self.__class__.__bases__
                    if issubclass(f, models.Field)][0]

            localized_field = self.base_class(
                format_lazy("{} ({})", self.verbose_name, lang_code),
                **params
            )

            localized_field.contribute_to_class(
                cls,
                "%s%s" % (name, lang_suffix(lang_code)),
            )

        setattr(cls, name, property(get_translated_value(name)))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.formfield_class,
        }
        defaults.update(kwargs)
        return super(TranslatableFieldMixin, self).formfield(**defaults)


class TranslatableCharField(TranslatableFieldMixin, models.CharField):
    pass


class TranslatableSlugField(TranslatableFieldMixin, models.SlugField):
    pass


class TranslatableFormField(forms.fields.CharField):
    # def __init__(self, *args, **kwargs):
        # kwargs.update({'widget': CKEditorWidget(config_name=config_name, extra_plugins=extra_plugins,
                                                # external_plugin_resources=external_plugin_resources)})
        # super(RichTextFormField, self).__init__(*args, **kwargs)
    pass


class TranslatableTextField(TranslatableFieldMixin, models.TextField):
    formfield_class = forms.fields.CharField


class TranslatableJSONField(TranslatableFieldMixin, JSONField):
    extra_parameter_names = ['encoder']


