"""hackinout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from inout.views import CustomCallback,UserDash,Index,logout_view,closed,home_view,team_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # The following urls have been disabled due to the change in registration process for InOut 3.0
    #url(r'^accounts/callback/(?P<provider>(\w|-)+)/$',CustomCallback.as_view(),name='mlh-callback'),
    #url(r'^accounts/profile/$',UserDash),
    #url(r'^accounts/logout/$',logout_view),
    #url(r'^accounts/', include('allaccess.urls')),
    url(r'^$',Index),
    url(r'^new/(?P<team_url_id>(\w{6}))$',team_view),
    url(r'^new$',home_view),
    url(r'^closed/',closed,name='closed')
]
