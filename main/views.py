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

from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from problem.models import Problem
from submission.models import Submission
from ums.models import Student


class HomeView(TemplateView):
    template_name = "main/main.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['problems'] = Problem.objects.all().order_by('order')
        context['submissions'] = Submission.objects.filter(submitter=self.request.user.student)
        context['title'] = _('Home')

        return context


class RankingProblemsView(TemplateView):
    template_name = "main/ranking.html"

    def get_context_data(self, **kwargs):
        context = super(RankingProblemsView, self).get_context_data(**kwargs)

        ranking = []
        submissions = Submission.objects.all()

        for problem in Problem.objects.all():
            recount = [x for x in submissions if x.problem == problem and x.status == 2].__len__()
            ranking.append((problem.order, recount))
            ranking.sort(key=lambda r: r[0])

        context['ranking'] = ranking

        return context


class RankingUsersView(TemplateView):
    template_name = "main/ranking.html"

    def get_context_data(self, **kwargs):
        context = super(RankingUsersView, self).get_context_data(**kwargs)

        ranking = []
        submissions = Submission.objects.all()

        for student in Student.objects.all():
            recount = sum([x.problem.points for x in submissions if x.submitter == student and x.status == 2])
            ranking.append((student.user.username, recount))
            ranking.sort(key=lambda r: r[1])

        context['ranking'] = ranking

        return context
