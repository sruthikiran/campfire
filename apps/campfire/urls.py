from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.splash),
    url(r'^log_reg$',views.log_reg),
    url(r'^wall$',views.wall),
    url(r'^profile$',views.profile),
    url(r'^editProfile$',views.editProfile),
    url(r'^updateProfile$',views.updateProfile),
    url(r'^network$',views.network),
    url(r'^qanda$',views.qanda),
    url(r'^addQuestion$',views.addQuestion),
    url(r'^createQuest$',views.createQuest),
    url(r'^createAns$',views.createAns),
    url(r'^(?P<number>\d+)\/addAnswer$',views.addAnswer),
    url(r'^inbox$',views.inbox),
    url(r'^newmess$',views.newmess),
    url(r'^createMsg$',views.createMsg),
    url(r'^delete/(?P<number>\d+)$',views.delMess),
    url(r'^reply/(?P<number>\d+)$',views.reply),
    url(r'^createReply$',views.createReply),
    url(r'^articles$',views.articles),
    url(r'^logout$',views.logout),
]
