# Generated by Django 4.2.1 on 2023-05-23 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_alter_ordermodel_dateendfact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='dateEndFact',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='discounts',
            field=models.ManyToManyField(blank=True, default=None, to='mainapp.discountmodel'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='penalties',
            field=models.ManyToManyField(blank=True, default=None, to='mainapp.penaltymodel'),
        ),
    ]
