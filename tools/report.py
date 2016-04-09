#!/usr/bin/python
#-*- coding: utf-8 -*-

from pos.models import *

contributors_for_type = {}
for contrib_type in ContributorType.objects.all():
    contributors_for_type[contrib_type] = Contributor.objects.filter(contrib_type=contrib_type)


for contrib_type, contributors in contributors_for_type.iteritems():
    print "Tipologia: %s" % contrib_type
    type_discounted = 0
    type_real = 0
    for contrib in contributors:
        print "\tNominativo: %s" % contrib
        orders = Order.objects.filter(contributor=contrib)
        total_discounted = 0
        total_real = 0
        for order in orders:
            amount_discounted = order.amount
            amount_real = sum(map(lambda p: p.amount, OrderPart.objects.filter(order=order)))
            total_discounted += amount_discounted
            total_real += amount_real
            print "\tOrdine %d: %.2f € (incassati) %.2f € (reali)" % (order.id, amount_discounted, amount_real)
        type_discounted += total_discounted
        type_real += total_real
        print "\t >>> Totale per %s: %.2f € (incassati) %.2f € (reali)" % (contrib, total_discounted, total_real)
        print
    print ">>> Totale per la tipologia %s: %.2f € (incassati) %.2f € (reali)" % (contrib_type, type_discounted, type_real)
    print

