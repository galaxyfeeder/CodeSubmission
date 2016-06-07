from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
            submission = Submission(problem=problem, submitter=request.user.student, code=request.FILES['code'],
                                    number=Submission.objects.filter(problem=problem,
                                                                     submitter=request.user.student).count()
                                    )
            submission.save()

        return redirect('submit', problem.pk)


@login_required
def serve_submission_file(request, *args, **kwargs):
    submission = Submission.objects.get(pk=kwargs.get('pk_submission', None))
    fsock = open(submission.code.path, 'r')
    response = HttpResponse(fsock)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=submission-' + str(submission.pk)
    return response


class SubmissionDetail(TemplateView):
    template_name = "submission/submission_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)

        context['submission'] = Submission.objects.get(pk=kwargs.get('pk_submission', None))

        return context


class SubmissionList(TemplateView):
    template_name = "submission/submission_list.html"

    def get_context_data(self, **kwargs):
        context = super(SubmissionList, self).get_context_data(**kwargs)

        context['submissions'] = Submission.objects.filter(submitter=self.request.user.student)
        context['problem'] = Problem.objects.get(pk=kwargs.get('pk', None))

        return context
