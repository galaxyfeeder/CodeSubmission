from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from problem.views import ProblemDetail

urlpatterns = [
    url(r'^problem/(?P<pk>\d+)$', login_required(ProblemDetail.as_view()), name='problem')
]
