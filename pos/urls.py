from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/save/$', views.save),
    re_path(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/(?P<contributor_id>\d+)/save/$', views.save),
    re_path(r'^checkout/(?P<checkout_id>\d+)/$', views.checkout),
    re_path(r'^checkout/$', views.select),
    re_path(r'^change/(?P<order_id>\d+)/payment_method/(?P<payment_method>\w)/$', views.change_payment_method),
    re_path(r'^print/(?P<order_id>\d+)/$', views.print_order),
    re_path(r'^report/$', views.report),
    re_path(r'^robots.txt$', views.robots),
    re_path(r'^$', views.home),
]
