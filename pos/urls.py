from django.conf.urls import patterns, include, url

urlpatterns = patterns('pos.views',
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/save/$', 'save'),
    url(r'^checkout/(?P<checkout_id>\d+)/(?P<payment_method>\w)/(?P<contributor_id>\d+)/save/$', 'save'),
    url(r'^checkout/(?P<checkout_id>\d+)/$', 'checkout'),
    url(r'^checkout/$', 'select'),
    url(r'^print/(?P<order_id>\d+)/$', 'print_order'),
    url(r'^report/$', 'report'),
    url(r'^robots.txt$', 'robots'),
    url(r'^$', 'home'),
)
