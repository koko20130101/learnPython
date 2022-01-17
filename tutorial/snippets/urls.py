# from django.conf.urls import url, include
from django.urls import  path


from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root, login


urlpatterns = [
    # url(r'^$', api_root),
    # url(r'^snippets/$', snippet_list, name='snippet-list'),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    # url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        # snippet_highlight, name='snippet-highlight'),
    # url(r'^users/$', user_list, name='user-list'),
    # url(r'^users/(?P<pk>[0-9]+)$', user_detail, name='user-detail'),
    path('login', login),
]
