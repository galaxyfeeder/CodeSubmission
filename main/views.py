from django.shortcuts import render
from django.views.generic import TemplateView

from problem.models import Problem
from submission.models import Submission


class HomeView(TemplateView):
    template_name = "main/main.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['problems'] = Problem.objects.all()
        context['submissions'] = Submission.objects.filter(submitter=self.request.user.student)

        return context
