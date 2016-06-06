from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from submission.views import SubmitView

urlpatterns = [
    url(r'^problem/(?P<pk>\d+)/submit$', login_required(SubmitView.as_view()), name='submit')
]
