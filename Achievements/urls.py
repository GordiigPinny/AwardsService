from django.conf.urls import url
from Achievements import views


urlpatterns = [
    url(r'^achievements/$', views.AchievementsListView.as_view()),
    url(r'^achievements/(?P<pk>\d+)/$', views.AchievementDetailView.as_view()),
]
