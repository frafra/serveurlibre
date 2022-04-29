# -*- coding: utf-8 -*-

from pos.models import Checkout, Product, ProductGroup, Contributor, Offer, Order, OrderPart, OrderPartDetail#, LiquidTransaction
from django.http import HttpResponse
#from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
import datetime
from .settings import *

# Cocidi speciali per la stampa su stampanti termiche di tipo Meteor Sprint B
sprint_b = {
    'line_length':48,
    'top':'\n',
    'bottom':'\n\n\n\n',
    'full_cut':'\x1b\x69',
    'partial_cut':'\x1b\x6d',
    #'double_height_on':'\x1b\x49',
    'double_height_on':'\x1b\x49\x1b\x21\x10',
    'reset':'\x1b\x40',
}

def home(request):
    return render(request, 'pos/home.html', {'title':"Pagina iniziale"})

def select(request):
    context = {}
    context['title'] = "Seleziona cassa"
    context['checkout'] = Checkout.objects.all().order_by('name')
    return render(request, 'pos/select.html', context)

first_value = lambda lst: [item[0] for item in lst]
def checkout(request, checkout_id):
    get_object_or_404(Checkout, pk=checkout_id)
    context = {}
    #context.update(csrf(request))
    context['title'] = "Cassa %s" % checkout_id
    products = Product.objects.all().order_by('position', 'name')
    categories = []
    for category in set(first_value(products.values_list('productgroup'))):
        categories.append(ProductGroup.objects.get(pk=category))
    contributors = Contributor.objects.valid_coupon().order_by('name')
    #topsellers = Product.objects.annotate(num_products=Sum('orderpartdetail__quantity')).order_by('-num_products')[:9]
    #topseller_width = int(100.0/(len(topsellers)/2+1))
    offers = []
    for offer in Offer.objects.filter(enabled=True).order_by('name'):
        offers.append([offer, offer.products.all()])
    offers_height = int(100.0/(len(offers)+1))
    payment_methods = (
        ("C", "Contanti"),
        ("P", "POS"),
    )
    context['products'] = products
    context['categories'] = categories
    context['contributors'] = contributors
    #context['topsellers'] = topsellers
    #context['topseller_width'] = topseller_width
    context['offers'] = offers
    context['offers_height'] = offers_height
    context['payment_methods'] = payment_methods
    return render(request, 'pos/checkout.html', context)

def save(request, payment_method, checkout_id, contributor_id=0):
    """ Funzione per il salvataggio dell'ordine """
    try:
        if request.method == 'POST':
            if len(request.POST) > 0:
                # Creazione dell'ordine
                if contributor_id != 0:
                    order = Order(checkout=Checkout.objects.get(pk=checkout_id),
                        contributor=Contributor.objects.get(pk=contributor_id),
                        payment_method=payment_method)
                else:
                    order = Order(checkout=Checkout.objects.get(pk=checkout_id),
                        payment_method=payment_method)
                order.save(lazy=True)
                # Parsing ed il processamento dei prodotti
                tmp = {}
                for product, quantity in request.POST.items():
                    if '-' in product: # Se '-' è presente significa che è stata associata una offerta
                        offer = int(product.split('-')[1])
                        # Raggruppa i prodotti in base all'offerta associata
                        if offer not in tmp:
                            tmp[offer] = {}
                        for product in Offer.objects.get(pk=offer).products.all():
                            tmp[offer][int(product.id)] = int(quantity)
                    else:
                        if 0 not in tmp: # Se non è stata associata una offerta, si crea una porzione di ordine vuota
                            tmp[0] = {}
                        tmp[0][int(product)] = int(quantity)
                # Salvataggio dei dettagli prodotto, porzioni di prodotto e associazione all'ordine
                for offer, values in tmp.items():
                    if offer == 0:
                        part = OrderPart(order=order)
                    else:
                        part = OrderPart(order=order, offer=Offer.objects.get(pk=offer))
                    part.save(lazy=True)
                    for product, quantity in values.items():
                        orderPartDetail = OrderPartDetail(
                            product=Product.objects.get(pk=product),
                            quantity=quantity, orderpart=part)
                        orderPartDetail.save(lazy=True)
                    part.save(lazy=True)
                order.save()
                return HttpResponse(order.id)
        return HttpResponse('ERROR')
    except:
        return HttpResponse('ERROR')

def change_payment_method(request, order_id, payment_method):
    order = Order.objects.get(pk=order_id)
    order.payment_method = payment_method
    order.save()
    return HttpResponse('OK')

def report(request):
    """ Codice per la generazione del report """
    # Codice disabilitato per la gestione del prelievo e dei vessamenti da/per le casse (LiquidTransaction)
    """checkout = Checkout.objects.all().order_by('name')
    transactions = {}
    for item in checkout:
        transactions[item] = Order.objects.filter(checkout=item.id).filter(payment_method="C").aggregate(Sum('amount'))['amount__sum'] or 0"""
    # Codice per la gestione delle statistiche giornaliere (prodotti venduti e relative quantità)
    today_orders = Order.objects.working_day()
    today_products = {}
    for detail in OrderPartDetail.objects.filter(orderpart__in=OrderPart.objects.filter(order__in=today_orders)):
        product = detail.product
        group = product.productgroup
        if group not in today_products:
            today_products[group] = {}
        if product not in today_products[group]:
            today_products[group][product] = 0
        old = today_products[group][product]
        today_products[group][product] += detail.quantity
    # Prodotti più venduti (di sempre)
    products = Product.objects.annotate(num_products=Sum('orderpartdetail__quantity'))
    topsellers = products.order_by('-num_products')[:10]
    # Incassi giornalieri
    today = today_orders.aggregate(Sum('amount'))['amount__sum'] or 0
    cash = today_orders.filter(payment_method="C").aggregate(Sum('amount'))['amount__sum'] or 0
    pos = today_orders.filter(payment_method="P").aggregate(Sum('amount'))['amount__sum'] or 0
    # Incassi totali
    orders = Order.objects.all()
    every = orders.aggregate(Sum('amount'))['amount__sum'] or 0
    every_cash = orders.filter(payment_method="C").aggregate(Sum('amount'))['amount__sum'] or 0
    every_pos = orders.filter(payment_method="P").aggregate(Sum('amount'))['amount__sum'] or 0
    # Riepilogo dei prodotti con le relative quantità vendute
    grouped = {}
    groups = ProductGroup.objects.all().order_by('name')
    for group in groups:
        grouped[group] = products.filter(productgroup=ProductGroup.objects.get(id=group.id)).order_by("name")
    
    context = {}
    context['title'] = "Report"
    #context['transactions'] = transactions
    context['products'] = products
    context['today_products'] = today_products
    context['topsellers'] = topsellers
    context['today'] = today
    context['cash'] = cash
    context['pos'] = pos
    context['every'] = every
    context['every_cash'] = every_cash
    context['every_pos'] = every_pos
    context['grouped'] = grouped
    return render(request, 'pos/report.html', context)

def print_order(request, order_id):
    """ Codice per la stampa dell'ordine """
    order = Order.objects.get(pk=order_id)
    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename=pos-%d.txt' % order.id
    response.write(sprint_b['top'])
    date = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S')
    orderparts = OrderPart.objects.filter(order=order_id)
    checkout = Checkout.objects.get(pk=order.checkout_id)
    details = {}
    # Creazione dello scontrino
    response.write(sprint_b['reset'])
    for line in TESTATA.strip().splitlines():
        if len(line) > sprint_b['line_length']:
            response_write(line)
        else:
            response.write(line.center(sprint_b['line_length']))
        response.write("\n")
    response.write("\n\n")
    response.write("%s %d %s\n\n" % (date, order.id, checkout))
    for orderpart in orderparts:
        orderpartdetails = OrderPartDetail.objects.filter(orderpart=orderpart)
        if orderpart.offer: # Gestione delle offerte
            for orderpartdetail in orderpartdetails:
                if orderpartdetail.product.productgroup not in details:
                    details[orderpartdetail.product.productgroup] = []
                details[orderpartdetail.product.productgroup].append("%dx %s (%s)\n" % (orderpartdetail.quantity, orderpartdetail.product, orderpart.offer))
            last=("%dx %s" % (orderpartdetail.quantity, orderpart.offer))
            response.write(last)
            response.write(("%.2f euro" % (orderpart.offer.price*orderpartdetail.quantity)).rjust(sprint_b['line_length']-len(last)))
            response.write("\n")
        else: # Gestione dei prodotti non associati alle offerte
            for orderpartdetail in orderpartdetails:
                if orderpartdetail.product.productgroup not in details:
                    details[orderpartdetail.product.productgroup] = []
                details[orderpartdetail.product.productgroup].append("%dx %s\n" % (orderpartdetail.quantity, orderpartdetail.product))
                last=("%dx %s" % (orderpartdetail.quantity, orderpartdetail.product))
                response.write(last)
                response.write(str("%.2f euro" % orderpartdetail.amount).rjust(sprint_b['line_length']-len(last)))
                response.write("\n")
    response.write("\n")
    last=">>> Totale"
    response.write(last)
    response.write(("%.2f euro" % order.amount).rjust(sprint_b['line_length']-len(last)))
    response.write("\n")
    if order.contributor:
        last=">>> Totale (non scontato)"
        response.write(last)
        amount=OrderPart.objects.filter(order=order_id).aggregate(Sum('amount'))['amount__sum'] or 0
        response.write(("%.2f euro" % amount).rjust(sprint_b['line_length']-len(last)))
        response.write("\n")
    # Creazione delle comande
    response.write(sprint_b['bottom'])
    response.write(sprint_b['partial_cut'])
    response.write(sprint_b['double_height_on'])
    for group, detail in details.items(): # Stampa della comanda divisa per categoria
        response.write("* Comanda *".center(sprint_b['line_length']))
        response.write("\n\n")
        response.write("%s %d %s\n\n" % (date, order.id, checkout))
        response.write(">>> %s\n\n" % group)
        for item in detail:
            response.write(item)
            response.write("\n\n")
        response.write(sprint_b['bottom'])
        response.write(sprint_b['partial_cut'])
    response.write(sprint_b['reset'])
    return response

def robots(request):
    """ Funzione per i crawler (indicizzazione permessa) """
    return HttpResponse("User-agent: *\nDisallow: \n")

