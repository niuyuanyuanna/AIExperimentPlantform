
from django.conf.urls import url,include
from django.contrib import admin
from webapp.views import index
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^web/', include('webapp.urls')),
    url(r'^docker/',include('dockermanager.urls')),
    url(r'^server/',include('servermanager.urls')),
   # url(r'^domain/', include('domainmanager.urls')),
    url(r'^salt/',include('saltadmin.urls')),
    url(r'^teach/',include('teachmanager.urls')),
    url(r'^learn/',include('learnmanager.urls')),
]
