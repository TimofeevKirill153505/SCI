# Generated by Django 4.2.1 on 2023-05-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_alter_ordermodel_dateendfact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='dateEndFact',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
