from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from review.forms import ReviewForm
from review.models import Review
from submission.models import Submission
from ums.models import Judge


class ReviewList(UserPassesTestMixin, TemplateView):

    def test_func(self):
        return Judge.objects.filter(user=self.request.user).count() != 0

    template_name = 'review/review_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewList, self).get_context_data(**kwargs)

        context['unrevised_submissions'] = Submission.objects.filter(status=0)
        context['on_progress_submissions'] = Submission.objects.filter(status=1)
        context['revised_submissions'] = Submission.objects.filter(status__gte=2)

        return context


class ReviewDetail(UserPassesTestMixin, TemplateView):
    template_name = 'review/review_detail.html'

    def test_func(self):
        return Judge.objects.filter(user=self.request.user).count() != 0

    def get_context_data(self, **kwargs):
        context = super(ReviewDetail, self).get_context_data(**kwargs)

        context['submission'] = Submission.objects.get(pk=kwargs.get('pk', None))
        context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        submission = Submission.objects.get(pk=kwargs.get('pk', None))

        if submission.status == 0:
            submission.status = 1
            submission.save()
            return redirect('review', submission.pk)
        elif submission.status == 1:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = Review(reviewer=request.user.judge,
                                submission=submission,
                                comment=request.POST['comment'])
                review.save()
                submission.status = request.POST['status']
                submission.save()
            return redirect('reviews')
