# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.test import TestCase
from django.utils import translation

from main.test_app.models import Entry


translation.activate('de')

Entry.objects.create(title_de="Deutscher Titel", title_en="English Title", description_de="Ein kleiner kurzer Text.", description_en="A short text.")

from django.core.management import call_command

call_command('rebuild_index')

