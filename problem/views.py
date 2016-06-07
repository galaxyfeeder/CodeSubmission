from django.shortcuts import render
from django.views.generic import TemplateView

from problem.models import Problem


class ProblemDetail(TemplateView):
    template_name = "problem/problem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProblemDetail, self).get_context_data(**kwargs)

        context['problem'] = problem = Problem.objects.get(pk=kwargs.get('pk', None))
        context['title'] = problem.title

        return context


class ProblemList(TemplateView):
    template_name = "problem/problem_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProblemList, self).get_context_data(**kwargs)

        context['problems'] = Problem.objects.all()

        return context
