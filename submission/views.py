from django.shortcuts import redirect
from django.views.generic import TemplateView

from problem.models import Problem
from submission.forms import SubmissionForm
from submission.models import Submission


class SubmitView(TemplateView):
    template_name = "submission/submit.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        context['problem'] = Problem.objects.get(pk=kwargs.get('pk', None))
        context['submit_form'] = SubmissionForm()

        return context

    def post(self, request, *args, **kwargs):
        problem = Problem.objects.get(pk=kwargs.get('pk', None))
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = Submission(problem=problem, submitter=request.user.student, code=request.FILES['code'])
            submission.save()

        return redirect('submit', problem.pk)
