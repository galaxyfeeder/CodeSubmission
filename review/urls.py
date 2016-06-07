from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from review.views import ReviewList, ReviewDetail

urlpatterns = [
    url(r'^reviews$', login_required(ReviewList.as_view()), name='reviews'),
    url(r'^reviews/(?P<pk>\d+)$', login_required(ReviewDetail.as_view()), name='review')
]
