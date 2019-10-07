# Generated by Django 2.2.5 on 2019-10-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCI', '0010_auto_20191006_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='last_taught',
            field=models.DateField(blank=True, null=True, verbose_name='Last Taught'),
        ),
        migrations.AlterField(
            model_name='course',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Most Recent Course Website'),
        ),
    ]