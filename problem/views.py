from django.shortcuts import render
from django.views.generic import TemplateView


class ProblemDetail(TemplateView):
    template_name = "problem/problem_detail.html"
