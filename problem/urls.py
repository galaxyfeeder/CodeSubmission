from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from problem.views import ProblemDetail, ProblemList

urlpatterns = [
    url(r'^problems$', login_required(ProblemList.as_view()), name='problems'),
    url(r'^problems/(?P<pk>\d+)$', login_required(ProblemDetail.as_view()), name='problem')
]
