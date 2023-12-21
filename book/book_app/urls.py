
from django.urls import re_path as url
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
import book_app.views as views


urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard")
]