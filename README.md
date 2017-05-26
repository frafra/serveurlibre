# serveurlibre
Simple POS based on Django which supports a couple of Meteor printers

This is a **personal project**, nothing professional, developed in 2012/2013, initially based on Django 1.4, then ported to Django 1.8.
I choose to publish the code on GitHub under a free software license because it makes no sense to me to keep it on my computer; maybe it could be useful for somebody else.

It contains some comments in Italian (sorry about that), it uses jQuery without any fancy Bootstrap-like framework.

Even if the code quality is not very high (there's plenty of room for optimization), the application works just fine: it has been able to manage about 100.000 orders using old computers without a hitch.

## Fedora kickstart file

In order to make it easier to distribute and use this program, I made a Fedora kickstart file (you can find it under *tools/serveurlibre.ks*; be sure to change paths accordingly with your configuration), which produces an unbranded Fedora XFCE Live respin with a single command, like:

```
# setarch i686 livecd-creator --verbose --config=$(pwd)/tools/serveurlibre.ks --fslabel=ServeurLibre --cache=/var/cache/live --releasever=25
```

Please make sure to have installed these dependencies:
```
# dnf install livecd-tools spin-kickstarts
```

You can download the [resulting ISO](http://experimental.frafra.eu/ServeurLibre.iso) if you want to try it (user/password for the Django admin interface are both set to *admin*).
