from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='accounts')),
    url(r'^', include('problem.urls')),
    url(r'^', include('submission.urls')),
    url(r'^', include('main.urls')),
    url(r'^', include('review.urls'))
]
