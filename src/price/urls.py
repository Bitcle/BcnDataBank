from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^1h', views.hour, name='hour')
]
