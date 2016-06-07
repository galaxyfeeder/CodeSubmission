from __future__ import unicode_literals

from django.db import models

from submission.models import Submission
from ums.models import Judge


class Review(models.Model):
    submission = models.ForeignKey(Submission)
    reviewer = models.ForeignKey(Judge)
    comment = models.TextField()
