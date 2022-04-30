# -*- coding: utf-8 -*-

import pos.models
from django.contrib.sites.models import Site
from django.contrib import admin
from django import forms

# Personalizzazione dell'interfaccia di amministrazione (filtri, campi da mostrare, campi nei quali cercare, ...)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')

# Codice commentato per la gestione di prelievi e versamenti di contante da/verso le casse
#class LiquidTransactionAdmin(admin.ModelAdmin):
#    list_display = ('checkout', 'amount', 'date')
#    list_filter = ['checkout']
#    date_hierarchy = 'date'

# Personalizzazione dell'interfaccia 
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'note')
    list_filter = ['name']

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contrib_type', 'contrib_group')
    list_filter = ['contrib_type', 'contrib_group']
    search_fields = ['name', 'note']

class ContributorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'coupon', 'note')

class ContributorGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'note')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'valid_order', 'checkout', 'contributor', 'amount',
        'payment_method', 'note')
    list_filter = ('checkout', 'contributor', 'payment_method')
    date_hierarchy = 'date'
    search_fields = ['contributor']

class OrderPartAdmin(admin.ModelAdmin):
    list_display = ('order', 'offer', 'valid_orderpart', 'amount')
    list_filter = ['offer']

class OrderPartDetailForm(forms.ModelForm):
    """ Codice speciale per la validazione dell'inserimento dei prodotti
        Qualora il prodotto non fosse disponibile o la quantità fosse nulla
            verrà restituito errore """
    class Meta:
        model = pos.models.OrderPartDetail
        exclude = []
    def clean_quantity(self):
        cleaned_data = super(OrderPartDetailForm, self).clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        if product.availability < quantity:
            raise forms.ValidationError("Prodotto non disponibile")
        if quantity == 0:
            raise forms.ValidationError("Inserire una quantità valida")
        return quantity

class OrderPartDetailAdmin(admin.ModelAdmin):
    form = OrderPartDetailForm
    list_display = ('orderpart', 'product', 'amount', 'quantity')
    list_filter = ['product']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'productgroup', 'position', 'availability')
    list_filter = ['productgroup', 'position', 'availability']

class ProductGroupAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(pos.models.Checkout, CheckoutAdmin)
admin.site.register(pos.models.Offer, OfferAdmin)
#admin.site.register(pos.models.LiquidTransaction, LiquidTransactionAdmin)
admin.site.register(pos.models.Contributor, ContributorAdmin)
admin.site.register(pos.models.ContributorType, ContributorTypeAdmin)
admin.site.register(pos.models.ContributorGroup, ContributorGroupAdmin)
admin.site.register(pos.models.Order, OrderAdmin)
admin.site.register(pos.models.OrderPart, OrderPartAdmin)
admin.site.register(pos.models.OrderPartDetail, OrderPartDetailAdmin)
admin.site.register(pos.models.Product, ProductAdmin)
admin.site.register(pos.models.ProductGroup, ProductGroupAdmin)

admin.site.unregister(Site)
