from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from submission.views import SubmitView, SubmissionDetail, SubmissionList

urlpatterns = [
    url(r'^problem/(?P<pk>\d+)/submit$', login_required(SubmitView.as_view()), name='submit'),
    url(r'^problem/(?P<pk>\d+)/submissions$', login_required(SubmissionList.as_view()), name='submissions'),
    url(r'^problem/(?P<pk>\d+)/submissions/(?P<pk_submission>\d+)$', login_required(SubmissionDetail.as_view()), name='submission'),
    url(r'^problem/(?P<pk>\d+)/submissions/(?P<pk_submission>\d+)/code$', login_required('submission.views.serve_submission_file'), name='code')
]
