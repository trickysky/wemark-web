from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^callback', views.authorize),
    url(r'^logout', views.logout),
]
