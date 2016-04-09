#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serveurlibre.settings")
from pos.models import Checkout, Contributor, ContributorType, ContributorGroup, ProductGroup, Product, Offer, Order, OrderPart, OrderPartDetail#, LiquidTransaction

import random

# Valori dai quali estrarre
letters = "abcdefghilmnopqrstuvzjkxyw"
booleans = [True, False]
colors = "blue red yellow green white black grey".split(" ")

# Generatori di prezzi, quantità, stringhe, ... casuali
makePrice = lambda: random.randrange(1, 10000, 1)/100.0
makeQuantity = lambda: random.randrange(-1, 5, 1)
makeString = lambda: "".join([random.choice(letters) for t in range(random.randrange(1, 16, 1))])
makeText = lambda: " ".join([makeString() for t in range(random.randrange(1, 32, 1))])
makeBool = lambda: random.choice(booleans)
makeInteger = lambda: random.randrange(0, 100, 1)
makeColor = lambda: random.choice(colors)

def createCheckout():
    Checkout(
        name=makeString(),
        position=makeString(),
    ).save()

def createContributorType():
    ContributorType(
        name=makeString(),
        coupon=makePrice(),
        onceaday=makeBool(),
        note=makeString(),
    ).save()

def createContributorGroup():
    ContributorGroup(
        name=makeString(),
        note=makeString(),
    ).save()

def createContributor():
    Contributor(
        name=makeString(),
        contrib_type=random.choice(ContributorType.objects.all()),
        contrib_group=random.choice(ContributorGroup.objects.all()),
        note=makeText(),
    ).save()

def createProductGroup():
    ProductGroup(
        name=makeString(),
    ).save()

def createProduct():
    Product(
        name=makeString(),
        price=makePrice(),
        productgroup=random.choice(ProductGroup.objects.all()),
        availability=True,
        position=makeInteger(),
        color=makeColor(),
        note=makeText(),
    ).save()

def createLiquidTransaction():
    LiquidTransaction(
        checkout=random.choice(Checkout.objects.all()),
        amount=-makePrice(),
        note=makeText(),
    ).save()

def createOrder():
    order=Order(
        checkout=random.choice(Checkout.objects.all()),
        contributor=random.choice(Contributor.objects.all()),
    )
    order.save(lazy=True)
    orderpart = OrderPart(
        order=order,
        #offer=random.choice(Offer.objects.all()),
    )
    orderpart.save(lazy=True)
    k = 5
    products = random.sample(Product.objects.all(), k)
    for t in range(k):
        OrderPartDetail(
            product=products.pop(),
            quantity=makeQuantity(),
            orderpart=orderpart,
        ).save(lazy=True)
    orderpart.save()

def populate(function, times):
    """ Esegue la funzione data "times" volte """
    for t in range(times):
        try:
            function()
        except:
            pass

def populateAll(functions, times):
    for function in functions:
        populate(function, times)

if __name__ == '__main__':
    populateAll([
        createProductGroup,
    ], 5)
    populateAll([
        createContributorType,
        createContributorGroup,
        createContributor,
        createCheckout,
        createProduct,
        #createLiquidTransaction,
    ], 25)
    for t in range(100):
        createOrder()
