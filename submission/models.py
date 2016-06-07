from __future__ import unicode_literals

import urlparse

from django.core.files.storage import FileSystemStorage
from django.db import models

from code_submission.settings import BASE_DIR
from problem.models import Problem
from ums.models import Student


class Submission(models.Model):
    problem = models.ForeignKey(Problem)
    submitter = models.ForeignKey(Student)
    code = models.FileField(storage=FileSystemStorage(location=urlparse.urljoin(BASE_DIR, 'static_server/protected')),
                            upload_to='submissions')
    STATUS_CHOICES = (
        (0, 'Not revised'),
        (1, 'Started revising'),
        (2, 'Revised and accepted'),
        (3, 'Revised and declined')
    )
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
