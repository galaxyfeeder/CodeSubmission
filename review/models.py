from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from submission.models import Submission


class Review(models.Model):
    submission = models.ForeignKey(Submission)
    reviewer = models.ForeignKey(User)
    comment = models.TextField()
