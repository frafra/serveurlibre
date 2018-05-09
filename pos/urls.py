from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/save/$', views.save),
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/(?P<contributor_id>\d+)/save/$', views.save),
    url(r'^checkout/(?P<checkout_id>\d+)/$', views.checkout),
    url(r'^checkout/$', views.select),
    url(r'^change/(?P<order_id>\d+)/payment_method/(?P<payment_method>\w)/$', views.change_payment_method),
    url(r'^print/(?P<order_id>\d+)/$', views.print_order),
    url(r'^report/$', views.report),
    url(r'^robots.txt$', views.robots),
    url(r'^$', views.home),
]
