# serveurlibre
Simple POS based on Django which supports a couple of Meteor printers

This is a **personal project**, nothing professional, developed in 2012/2013, initially based on Django 1.4/Python 2, then ported to Django 2.0/Python 3 and more recently to Django 4.0.
I choose to publish the code on GitHub under a free software license because it makes no sense to me to keep it on my computer; maybe it could be useful for somebody else.

It contains some comments in Italian (sorry about that), it uses jQuery without any fancy Bootstrap-like framework.

Even if the code quality is not very high (there's plenty of room for optimization), the application works just fine: it has been able to manage about 100.000 orders using old computers without a hitch.

## Fedora kickstart file

In order to make it easier to distribute and use this program, I made a Fedora kickstart file (you can find it under *tools/serveurlibre.ks*; be sure to change paths accordingly with your configuration), which produces an unbranded Fedora XFCE Live respin with a single command, like:

Please make sure to have installed these dependencies:

```
# dnf install livecd-tools git
# livecd-creator --verbose --config=$(pwd)/tools/serveurlibre-flat.ks --fslabel=ServeurLibre --cache=/var/cache/live --releasever=34
```

In order to produce a new flattened kickstart file, this procedure can be used:

```
# dnf install fedora-kickstarts  # edit /usr/share/spin-kickstarts/fedora-repo.ks
$ ksflatten --config tools/serveurlibre.ks -o tools/serveurlibre-flat.ks --version F34
```

## Demo

user/password for the Django admin interface are both set to *admin*.
