# Generated by Django 4.2.3 on 2023-07-14 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-id',), 'verbose_name': 'Categories'},
        ),
    ]
