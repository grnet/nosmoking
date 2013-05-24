from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       # ex: /polls/5/
                       url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
                       # ex: /polls/5/results/
                       url(r'^(?P<poll_id>\d+)/results/$',
                           views.results, name='results'),
                       # ex: /polls/5/answer/
                       url(r'^(?P<poll_id>\d+)/answer/$',
                           views.answer, name='answer'),
                       url(r'^(?P<poll_id>\d+)/sign/$',
                           views.sign, name='sign')
)
