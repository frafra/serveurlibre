from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/save/$', views.save),
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/(?P<contributor_id>\d+)/save/$', views.save),
    url(r'^checkout/(?P<checkout_id>\d+)/$', views.checkout),
    url(r'^checkout/$', views.select),
    url(r'^print/(?P<order_id>\d+)/$', views.print_order),
    url(r'^report/$', views.report),
    url(r'^robots.txt$', views.robots),
    url(r'^$', views.home),
]
