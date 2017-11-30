"""db2_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from posts import views as posts_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', posts_views.signup, name='signup'),
    url(r'^account_activation_sent/$', posts_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        posts_views.activate, name='activate'),
    url(r'^index/(?P<order_by>asc|desc)/$', posts_views.index, name='home_sorted'),
    url(r'^index/$', posts_views.index, name='home'),
    url(r'^post/(?P<post_id>[0-9]+)/$', posts_views.detail, name='detail'),
    url(r'^post/(?P<pk>\d+)/comment/$', posts_views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^like/(?P<post_id>[0-9]+)$', posts_views.add_like, name='add_like'),
    url(r'^dislike/(?P<post_id>[0-9]+)$', posts_views.remove_like, name='remove_like'),
    url(r'^$', posts_views.index, name='home_default'),


]
