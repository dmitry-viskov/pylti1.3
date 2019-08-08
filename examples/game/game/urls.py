from django.conf.urls import url
from .views import login, launch, configure, score, scoreboard

urlpatterns = [
    url(r'^login/$', login, name='game-login'),
    url(r'^launch/$', launch, name='game-launch'),
    url(r'^configure/(?P<launch_id>[\w-]+)/(?P<difficulty>[\w-]+)/$', configure, name='game-configure'),
    url(r'^api/score/(?P<launch_id>[\w-]+)/(?P<earned_score>[\w-]+)/(?P<time_spent>[\w-]+)/$', score,
        name='game-api-score'),
    url(r'^api/scoreboard/(?P<launch_id>[\w-]+)/$', scoreboard, name='game-api-scoreboard'),
]
