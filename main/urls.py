from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from main.views import HomeView

urlpatterns = [
    url(r'^', login_required(HomeView.as_view()), name='home')
]
