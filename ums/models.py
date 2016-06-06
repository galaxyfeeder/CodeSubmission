from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User)


class Judge(models.Model):
    user = models.OneToOneField(User)
