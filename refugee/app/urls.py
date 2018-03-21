from . import views
from django.conf.urls import url

app_name = 'app'
urlpatterns = [
    url(r'^ngo_register/$', views.ngo_register, name='ngo_register'),
    url(r'^user_register/$', views.register, name='register'),
    url(r'^user_login/$', views.login, name='login'),
    url(r'^user_logout/$', views.logout, name='logout'),
    url(r'^ngo_login/$', views.ngo_login, name='ngo_login'),
    url(r'^ngo_profile/(?P<pk>[0-9]+)/$', views.ngo_profile, name='ngo_profile'),
    url(r'^ngo_logout/$', views.ngo_logout, name='ngo_logout'),
    url(r'^refugee_profile/(?P<idx>[0-9]+)/$', views.profile, name='profile'),
    url(r'^petition/ngo/create/$', views.create_ngo_petition, name='create_ngo_petition'),
    url(r'^petition/ngo/(?P<pk>[0-9]+)/$', views.view_ngo_petition, name='view_ngo_petition'),
    url(r'^petition/ngo/(?P<pk>[0-9]+)/vote/$', views.vote_ngo_petition, name='vote_ngo_petition'),
    url(r'^vote_message/$', views.vote_message, name='vote_message'),
    url(r'^petition/ngo/vote/(?P<pk>[0-9]+)/success/$', views.confirm_email, name='confirm'),
    url(r'^askforhelp/$', views.askforhelp, name='askforhelp'),
    url(r'^search/ngo/$', views.search_ngo, name='search_ngo'),
    url(r'^search/refugee/$', views.search_refugee, name='search_refugee'),
    url(r'^add/notification/$', views.add_notif, name='add_notif'),
    url(r'^all/notification/$', views.allnotifs, name='allnotifs'),
    url(r'^add/event/$', views.add_event, name='add_event'),
    url(r'^all/event/$', views.all_event, name='all_event'),
    url(r'^petition/refugee/(?P<pk>[0-9]+)/$', views.view_refugee_petition, name='view_refugee_petition'),
    url(r'^petition/refugee/vote/(?P<pk>[0-9]+)/success/$', views.refugee_confirm_email, name='refugee_confirm'),

]
