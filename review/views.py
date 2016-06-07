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
