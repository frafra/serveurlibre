from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles import views
admin.autodiscover()

import os

urlpatterns = [
    url(r'^static/(?P<path>.*)$', views.serve),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    
    # Custom
    url(r'^', include('pos.urls')),
]
