# Generated by Django 4.0.4 on 2022-04-30 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Esempi: Cassa principale, Cassa secondaria', max_length=64, unique=True, verbose_name='Nome')),
                ('position', models.TextField(blank=True, help_text='Esempi: Ingresso, Bar', verbose_name='Posizione')),
            ],
            options={
                'verbose_name': 'cassa',
                'verbose_name_plural': 'casse',
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Identificativo')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
            ],
            options={
                'verbose_name': 'partecipante',
                'verbose_name_plural': 'partecipanti',
            },
        ),
        migrations.CreateModel(
            name='ContributorGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Esempi: Circolo PD di Melzo, Arci di Pessano', max_length=64, unique=True, verbose_name='Nome')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
            ],
            options={
                'verbose_name': 'gruppo di partecipanti',
                'verbose_name_plural': 'gruppi di partecipanti',
            },
        ),
        migrations.CreateModel(
            name='ContributorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Esempi: Ospiti, Volontari, Musicisti', max_length=64, unique=True, verbose_name='Nome')),
                ('coupon', models.DecimalField(decimal_places=2, help_text='Esempi: 5, 3.99, 2.5', max_digits=8, verbose_name='Valore coupon')),
                ('onceaday', models.BooleanField(default=True, help_text='Se non attivo, il coupon sarà virtualmente infinito', verbose_name='Utilizzabile una volta al giorno')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
            ],
            options={
                'verbose_name': 'tipologia partecipanti',
                'verbose_name_plural': 'tipologie di partecipanti',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, help_text='Esempi: 3.5, 7.99, 4', max_digits=8, verbose_name='Prezzo')),
                ('enabled', models.BooleanField(default=True, help_text='Se non attiva, non sarà mostrata nelle casse', verbose_name='Attiva')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
            ],
            options={
                'verbose_name': 'offerta',
                'verbose_name_plural': 'offerte',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Data')),
                ('amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, verbose_name='Totale')),
                ('payment_method', models.CharField(choices=[('C', 'Contanti'), ('P', 'POS')], default='C', max_length=1, verbose_name='Metodo di pagamento')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('valid_order', models.BooleanField(default=False, editable=False, verbose_name='Ordine valido')),
                ('bonus', models.DecimalField(decimal_places=2, editable=False, max_digits=8, null=True, verbose_name='Sconto rimanente')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.checkout', verbose_name='Cassa')),
                ('contributor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos.contributor', verbose_name='partecipante')),
            ],
            options={
                'verbose_name': 'ordine',
                'verbose_name_plural': 'ordini',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='OrderPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=None, editable=False, max_digits=8, null=True, verbose_name='Totale')),
                ('valid_orderpart', models.BooleanField(default=False, editable=False, verbose_name='Porzione di ordine valida')),
                ('offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.offer', verbose_name='offerta')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.order', verbose_name='ordine')),
            ],
            options={
                'verbose_name': 'porzione ordine',
                'verbose_name_plural': 'porzioni ordini',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Esempi: Primi, Secondi, Contorni, Bevande', max_length=64, unique=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'gruppo di prodotti',
                'verbose_name_plural': 'gruppi di prodotti',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Esempi: Cotoletta alla milanese, pasta al sugo', max_length=64, unique=True, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, help_text='Esempi: 3.5, 7.99, 4', max_digits=8, verbose_name='Prezzo')),
                ('availability', models.PositiveIntegerField(blank=True, help_text='Non sarà possibile vendere prodotti se non disponibile', null=True, verbose_name='Disponibilità')),
                ('position', models.IntegerField(blank=True, help_text="Indica l'ordinamento rispetto agli altri prodotti", null=True, verbose_name='Posizione')),
                ('color', models.CharField(blank=True, help_text='Esempi: blue, red, #FF00FF', max_length=32, null=True, verbose_name='Colore')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('productgroup', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.productgroup', verbose_name='gruppo di prodotti')),
            ],
            options={
                'verbose_name': 'prodotto',
                'verbose_name_plural': 'prodotti',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='offer',
            name='products',
            field=models.ManyToManyField(to='pos.product', verbose_name='prodotti'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='contrib_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos.contributorgroup', verbose_name='gruppo di partecipanti'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='contrib_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.contributortype', verbose_name='tipologia partecipanti'),
        ),
        migrations.CreateModel(
            name='OrderPartDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=64, null=True)),
                ('quantity', models.IntegerField(verbose_name='Quantità')),
                ('amount', models.DecimalField(decimal_places=2, default=None, editable=False, max_digits=8, null=True, verbose_name='Totale')),
                ('orderpart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.orderpart', verbose_name='porzione ordine')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.product', verbose_name='prodotto')),
            ],
            options={
                'verbose_name': 'dettaglio ordine',
                'verbose_name_plural': 'dettaglio ordini',
                'unique_together': {('product', 'orderpart')},
            },
        ),
    ]
