"""
Copyright (c) 2016 Gabriel Esteban

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
    number = models.IntegerField(default=1)

    def __unicode__(self):
        return self.problem.__unicode__() + ' #' + str(self.number)
