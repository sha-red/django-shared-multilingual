# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from utils.fields import TranslatableCharField, TranslatableTextField


@python_2_unicode_compatible
class Category(models.Model):
    title = TranslatableCharField(_("Title"), max_length=200)

    class Meta:
        verbose_name = _("Entry Category")
        verbose_name_plural = _("Entry Categories")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Entry(models.Model):
    title = TranslatableCharField(
        _("Title"),
        max_length=200,
    )
    description = TranslatableTextField(
        _("Description"),
        blank=True,
    )
    categories = models.ManyToManyField(Category,
        verbose_name=_("Categories"), blank=True,
        related_name="ideas")

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __str__(self):
        return self.title

    def get_url_path(self):
        try:
            return reverse("idea_detail", kwargs={"id": self.pk})
        except NoReverseMatch:
            return ""
