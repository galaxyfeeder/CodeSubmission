from __future__ import unicode_literals

from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()


class TestCase(models.Model):
    problem = models.ForeignKey(Problem)
    input = models.TextField()
    output = models.TextField()
