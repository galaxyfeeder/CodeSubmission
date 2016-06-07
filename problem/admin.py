from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from problem.models import Problem
from problem.models import TestCase


class TestCaseInline(admin.StackedInline):
    model = TestCase
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }


class ProblemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }
    inlines = [TestCaseInline]

admin.site.register(Problem, ProblemAdmin)
