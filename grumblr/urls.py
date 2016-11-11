"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views

import grumblr.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', grumblr.views.home, name='home'),
    url(r'^register/', grumblr.views.register_user, name='register'),
    url(r'^post/', grumblr.views.post, name='post'),
    url(r'^account/', grumblr.views.myaccount, name='account'),
    url(r'^add-user', grumblr.views.register_user, name='register_user'),
    # url(r'^login$', auth_views.login, {'template_name':'grumblr/guest_home.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^post-new', grumblr.views.post, name='post_new'),
    url(r'^profile(?P<profile_id>[0-9]+)/$', grumblr.views.profile, name='profile'),
    url(r'^edit/', grumblr.views.edit, name='edit'),
    url(r'^changepassword/', grumblr.views.changepassword, name='changepassword'),
    url(r'^follow/(?P<profile_id>[0-9]+)/$', grumblr.views.follow, name='follow'),
    url(r'^unfollow/(?P<profile_id>[0-9]+)/$', grumblr.views.unfollow, name='unfollow'),
    url(r'^photo(?P<profile_id>[0-9]+)/$', grumblr.views.photo, name='photo'),
    url(r'^followstream/', grumblr.views.followstream, name='followstream'),
    url(r'^delete/(?P<blog_id>[0-9]+)/$', grumblr.views.blog_delete, name='blog_delete'),
    url(r'^confirm/(?P<name>[0-9A-Za-z_\-]+)\\(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', grumblr.views.confirm, name='confirm'),
    url(r'^forgetpassword/', grumblr.views.forgetpassword, name='forgetpassword'),
    url(r'^reset/(?P<name>[0-9A-Za-z_\-]+)\\(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', grumblr.views.reset, name='reset'),

    url(r'^get-posts/', grumblr.views.get_posts),
    url(r'^get-changes/(?P<time>.+)$', grumblr.views.get_changes),
    url(r'^comment/(?P<blog_id>\d+)$', grumblr.views.comment),
]
