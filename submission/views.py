from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from problem.models import Problem
from submission.forms import SubmissionForm
from submission.models import Submission
from ums.models import Student, Judge


class SubmitView(UserPassesTestMixin, TemplateView):

    def test_func(self):
        return Student.objects.filter(user=self.request.user).count() != 0

    template_name = "submission/submit.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        context['problem'] = problem = Problem.objects.get(pk=kwargs.get('pk', None))
        context['submit_form'] = SubmissionForm()
        context['submissions'] = subs = Submission.objects.filter(problem=problem, submitter=self.request.user.student)
        context['can_submit'] = ([x for x in subs if x.status <= 1].__len__() == 0)

        return context

    def post(self, request, *args, **kwargs):
        problem = Problem.objects.get(pk=kwargs.get('pk', None))
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = Submission(problem=problem, submitter=request.user.student, code=request.FILES['code'],
                                    number=Submission.objects.filter(problem=problem,
                                                                     submitter=request.user.student).count()+1
                                    )
            submission.save()

        return redirect('submission', problem.pk, submission.pk)


@login_required
def serve_submission_file(request, *args, **kwargs):
    if Judge.objects.filter(user=request.user).count() != 0 or Student.objects.filter(user=request.user).count() != 0 and request.user == Submission.objects.get(pk=kwargs.get('pk_submission', None)).submitter.user:
        submission = Submission.objects.get(pk=kwargs.get('pk_submission', None))
        fsock = open(submission.code.path, 'r')
        response = HttpResponse(fsock)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=submission-' + str(submission.pk)
        return response
    else:
        raise PermissionDenied


class SubmissionDetail(UserPassesTestMixin, TemplateView):
    template_name = "submission/submission_detail.html"

    def test_func(self):
        return Student.objects.filter(user=self.request.user).count() != 0 and self.request.user == Submission.objects.get(pk=self.kwargs.get('pk_submission', None)).submitter.user

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)

        context['submission'] = Submission.objects.get(pk=kwargs.get('pk_submission', None))

        return context


class SubmissionList(UserPassesTestMixin, TemplateView):
    template_name = "submission/submission_list.html"

    def test_func(self):
        return Student.objects.filter(user=self.request.user).count() != 0

    def get_context_data(self, **kwargs):
        context = super(SubmissionList, self).get_context_data(**kwargs)

        context['problem'] = problem = Problem.objects.get(pk=kwargs.get('pk', None))
        context['submissions'] = Submission.objects.filter(submitter=self.request.user.student, problem=problem)

        return context
