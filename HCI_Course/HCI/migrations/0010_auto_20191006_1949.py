# Generated by Django 2.2.5 on 2019-10-07 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCI', '0009_auto_20191006_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='prerequisites',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Course Prerequisites'),
        ),
    ]
