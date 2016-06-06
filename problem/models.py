from __future__ import unicode_literals

from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem)
    input = models.TextField()
    output = models.TextField()
