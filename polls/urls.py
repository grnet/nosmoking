from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<poll_id>\d+)/results/$',
                           views.results, name='results'),
                       url(r'^(?P<poll_id>\d+)/answer/(?P<user_uuid>.+)/$',
                           views.answer, name='answer'),
                       url(r'^(?P<poll_id>\d+)/sign/(?P<user_uuid>.+)/$',
                           views.sign, name='sign'),
                       url(r'^(?P<poll_id>\d+)/thanks/(?P<user_uuid>.+)/$',
                           views.thanks, name='thanks'),                       
                       url(r'^(?P<poll_id>\d+)/(?P<user_uuid>.+)/$',
                           views.detail, name='detail'),                       
)
