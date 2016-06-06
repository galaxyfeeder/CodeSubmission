from django.contrib import admin

from problem.models import Problem
from problem.models import TestCase

admin.site.register(Problem)
admin.site.register(TestCase)
