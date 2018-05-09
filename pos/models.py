# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils import timezone
from django.db.models import Count, Sum, Manager
import datetime

# Definizione dei modelli

@python_2_unicode_compatible
class ProductGroup(models.Model):
    name = models.CharField(unique=True,
        max_length=64, verbose_name="Nome",
        help_text="Esempi: Primi, Secondi, Contorni, Bevande")

    class Meta:
        verbose_name = "gruppo di prodotti"
        verbose_name_plural = "gruppi di prodotti"
        ordering = ['name']

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Checkout(models.Model):
    name = models.CharField(unique=True,
        max_length=64, verbose_name="Nome",
        help_text="Esempi: Cassa principale, Cassa secondaria")
    position = models.TextField(blank=True, verbose_name="Posizione",
        help_text="Esempi: Ingresso, Bar")

    class Meta:
        verbose_name = "cassa"
        verbose_name_plural = "casse"

    def __str__(self):
        return self.name

#@python_2_unicode_compatible
#class LiquidTransaction(models.Model):
#    checkout = models.ForeignKey(Checkout,
#        verbose_name=Checkout._meta.verbose_name)
#    amount = models.DecimalField(max_digits=8,
#        decimal_places=2, verbose_name="Contante immesso o prelevato",
#        help_text="Esempi: -30 (prelievo), 7.99 (immissione)")
#    date = models.DateTimeField(auto_now=True,
#        verbose_name="Orario")
#    note = models.TextField(blank=True, verbose_name="Note")
#
#    class Meta:
#        verbose_name = "transazione contante"
#        verbose_name_plural = "transazioni contante"
#
#    def __str__(self):
#        return str(timezone.make_naive(self.date,
#            timezone.get_default_timezone()))

@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(unique=True,
        max_length=64, verbose_name="Nome",
        help_text="Esempi: Cotoletta alla milanese, pasta al sugo")
    price = models.DecimalField(max_digits=8,
        decimal_places=2, verbose_name="Prezzo",
        help_text="Esempi: 3.5, 7.99, 4")
    productgroup = models.ForeignKey(ProductGroup,
        verbose_name=ProductGroup._meta.verbose_name,
        on_delete=models.PROTECT)
    availability = models.BooleanField(
        verbose_name="Disponibilità", default=True,
        help_text="Non sarà possibile vendere prodotti se non disponibile")
    position = models.IntegerField(
        verbose_name="Posizione", blank=True, null=True,
        help_text="Indica l'ordinamento rispetto agli altri prodotti")
    color = models.CharField(
        max_length=32, verbose_name="Colore", blank=True, null=True,
        help_text="Esempi: blue, red, #FF00FF")
    note = models.TextField(blank=True, verbose_name="Note")
    
    class Meta:
        verbose_name = "prodotto"
        verbose_name_plural = "prodotti"
        ordering = ['name']
        
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Offer(models.Model):
    name = models.CharField(unique=True, max_length=64,
        verbose_name="Nome")
    price = models.DecimalField(max_digits=8,
        decimal_places=2, verbose_name="Prezzo",
        help_text="Esempi: 3.5, 7.99, 4")
    products = models.ManyToManyField(Product,
        verbose_name=Product._meta.verbose_name_plural)
    enabled = models.BooleanField(default=True,
        verbose_name="Attiva",
        help_text="Se non attiva, non sarà mostrata nelle casse")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        verbose_name = "offerta"
        verbose_name_plural = "offerte"

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class ContributorGroup(models.Model):
    name = models.CharField(unique=True, max_length=64,
        verbose_name="Nome",
        help_text="Esempi: Circolo PD di Melzo, Arci di Pessano")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        verbose_name = "gruppo di partecipanti"
        verbose_name_plural = "gruppi di partecipanti"

    def __str__(self):
        return self.name
        
@python_2_unicode_compatible
class ContributorType(models.Model):
    name = models.CharField(unique=True, max_length=64,
        verbose_name="Nome",
        help_text="Esempi: Ospiti, Volontari, Musicisti")
    coupon = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name="Valore coupon",
        help_text="Esempi: 5, 3.99, 2.5")
    onceaday = models.BooleanField(default=True,
        verbose_name="Utilizzabile una volta al giorno",
        help_text="Se non attivo, il coupon sarà virtualmente infinito")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        verbose_name = "tipologia partecipanti"
        verbose_name_plural = "tipologie di partecipanti"

    def __str__(self):
        return self.name

class ContributorManager(models.Manager):
    def valid_coupon(self):
        """ Funzione per definire la validità del coupon """
        #query_set = super(ContributorManager, self).get_query_set()
        query_set = self.all() # Django >= 1.6
        for item in query_set:
            if item.contrib_type.onceaday:
                order = Order.objects.working_day().filter(contributor=item.id)
                if len(order)>0:
                    query_set = query_set.exclude(pk=item.id)
        return query_set
                        
@python_2_unicode_compatible
class Contributor(models.Model):
    name = models.CharField(unique=True, max_length=64,
        verbose_name="Identificativo")
    contrib_type = models.ForeignKey(ContributorType,
        verbose_name=ContributorType._meta.verbose_name,
        on_delete=models.PROTECT)
    contrib_group = models.ForeignKey(ContributorGroup,
        verbose_name=ContributorGroup._meta.verbose_name,
        blank=True, null=True,
        on_delete=models.SET_NULL)
    note = models.TextField(blank=True, verbose_name="Note")
    objects = ContributorManager()
    
    class Meta:
        verbose_name = "partecipante"
        verbose_name_plural = "partecipanti"

    def __str__(self):
        return self.name

def when_clock_was_at(hours):
    date = timezone.now().replace(hour=hours, minute=0, second=0, microsecond=0)
    if timezone.now() < date:
        date -= datetime.timedelta(days=1)
    return date

class OrderManager(models.Manager):
    def working_day(self):
        #return super(OrderManager, self).get_query_set().filter(date__gt=when_clock_was_at(6)) # UTC +2
        return self.all().filter(date__gt=when_clock_was_at(6)) # Django >= 1.6

first_value = lambda lst: [item[0] for item in lst]
@python_2_unicode_compatible
class Order(models.Model):
    date = models.DateTimeField(null=True, blank=True,
        verbose_name="Data")
    checkout = models.ForeignKey(Checkout,
        verbose_name="Cassa", on_delete=models.PROTECT)
    contributor = models.ForeignKey(Contributor,
        verbose_name=Contributor._meta.verbose_name,
        null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=8,
        decimal_places=2, verbose_name="Totale",
        default=0, editable=False)
    payment_method = models.CharField(max_length=1, choices=(
        ("C", "Contanti"),
        ("T", "Carta di credito"),
        ("B", "Bancomat"),
        ("A", "Altro"),
    ), verbose_name="Metodo di pagamento", default="C")
    note = models.TextField(blank=True, verbose_name="Note")
    objects = OrderManager()
 
    valid_order = models.BooleanField(default=False, editable=False,
        verbose_name="Ordine valido")
    
    bonus = models.DecimalField(max_digits=8,
        decimal_places=2, verbose_name="Sconto rimanente",
        null=True, editable=False)

    def apply_discount(self):
        """ Applicazione dello sconto """
        if self.bonus == None:
            self.bonus = self.contributor.contrib_type.coupon
        if self.bonus <= self.amount:
            self.amount -= self.bonus
            self.bonus = 0
        else:
            self.bonus -= self.amount
            self.amount = 0

    def save(self, lazy=False):
        if self.id == None:
            self.date = timezone.now()
        if not lazy: # "lazy" permette di bypassare la validazione nel caso non si fosse finito di creare l'ordine
            # Ordine valido se e solo se tutte le porzioni di ordine sono valide
            self.valid_order = all(first_value(OrderPart.objects.filter(order=self.id).values_list('valid_orderpart')))
            self.amount = OrderPart.objects.filter(order=self.id).aggregate(Sum('amount'))['amount__sum'] or 0
            if self.contributor != None:
                if self.contributor.contrib_type.coupon == 0:
                    pass
                elif self.contributor.contrib_type.onceaday:
                    order_list = Order.objects.working_day().exclude(pk=self.id).filter(contributor=self.contributor.id)
                    self.bonus = self.contributor.contrib_type.coupon
                    if order_list.exists():
                        self.contributor = None # Is it ok?
                    else:
                        self.apply_discount()
                else:
                    self.amount = 0
        else:
            self.valid_order = True
            self.amount = 0
        super(Order, self).save()
        
    class Meta:
        verbose_name = "ordine"
        verbose_name_plural = "ordini"
        ordering = ['-date']

    def __str__(self):
        return str(timezone.make_naive(self.date,
            timezone.get_default_timezone()))

@python_2_unicode_compatible
class OrderPart(models.Model):
    order = models.ForeignKey(Order,
        verbose_name=Order._meta.verbose_name,
        on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer,
        verbose_name=Offer._meta.verbose_name,
        on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name="Totale",
        null=True, default=None, editable=False)
    
    valid_orderpart = models.BooleanField(default=False, editable=False,
        verbose_name="Porzione di ordine valida")

    def save(self, lazy=False):
        if self.id != None: # Porzione di ordine già creata, si procede alla eventuale gestione dell'offerta
            if self.offer:
                details = OrderPartDetail.objects.filter(orderpart=self.id)
                if len(details) == 0:
                    self.valid_orderpart = False
                else:
                    if len(details.values('quantity').distinct())>1:
                        self.valid_orderpart = False
                    else:
                        offer_products = first_value(self.offer.products.all().values_list('id'))
                        products = first_value(details.values_list('product'))
                        self.valid_orderpart = set(offer_products) == set(products)
            else:
                self.valid_orderpart = True
            if self.offer and self.valid_orderpart:
                self.amount = self.offer.price*details[0].quantity
            else:
                self.amount = OrderPartDetail.objects.filter(orderpart=self.id).aggregate(Sum('amount'))['amount__sum'] or 0
        else:
            self.valid_orderpart = True
            self.amount = 0
        super(OrderPart, self).save()
        if not lazy:
            self.order.save()
        
    def delete(self):
        self.amount = 0
        self.order.save()
        super(OrderPart, self).delete()
 
    class Meta:
        verbose_name = "porzione ordine"
        verbose_name_plural = "porzioni ordini"

    def __str__(self):
        return "%s - %s" % (self.order, self.offer or "(nessuno)")

@python_2_unicode_compatible
class OrderPartDetail(models.Model):
    name = models.CharField(null=True,
        max_length=64, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
        verbose_name=Product._meta.verbose_name, null=True)
    quantity = models.IntegerField(verbose_name="Quantità")
    orderpart = models.ForeignKey(OrderPart,
        verbose_name=OrderPart._meta.verbose_name,
        on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name="Totale",
        null=True, default=None, editable=False)
    
    def save(self, lazy=False):
        if self.product:
            if self.quantity == 0:
                if self.id != None:
                    super(OrderPartDetail, self).delete()
            else:
                self.name = self.product.name
                self.amount = self.quantity*self.product.price
                super(OrderPartDetail, self).save()
                if not lazy:
                    self.orderpart.save()
    
    class Meta:
        verbose_name = "dettaglio ordine"
        verbose_name_plural = "dettaglio ordini"
        unique_together = ('product', 'orderpart')

    def __str__(self):
        return "%s - %s" % (self.orderpart, self.product)
