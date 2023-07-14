# Generated by Django 4.2.3 on 2023-07-14 10:59

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_product_name_products_name_and_more'),
        ('organizations', '0003_organizationconnection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_no', models.CharField(max_length=30)),
                ('village', models.CharField(max_length=100)),
                ('post_office', models.CharField(max_length=10)),
                ('thana', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='organization_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='organization',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='store.category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, max_length=255, populate_from='name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organizationemployee',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, max_length=255, populate_from='user__email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.address'),
        ),
    ]
