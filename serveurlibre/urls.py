from django.conf.urls import include
from django.urls import re_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles import views
admin.autodiscover()

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', views.serve),

    # Uncomment the admin/doc line below to enable admin documentation:
    #re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),
    
    # Custom
    re_path(r'^', include('pos.urls')),
]
