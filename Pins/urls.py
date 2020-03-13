from django.conf.urls import url
from Pins import views


urlpatterns = [
    url(r'^pins/$', views.PinListView.as_view()),
    url(r'^pins/(?P<pk>\d+)/$', views.PinDetailView.as_view()),
]
