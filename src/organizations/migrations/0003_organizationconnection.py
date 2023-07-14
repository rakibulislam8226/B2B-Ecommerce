# Generated by Django 4.2.3 on 2023-07-14 06:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_alter_organization_options_organizationemployee'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('connection_type', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=255)),
                ('from_organization', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='from_organization', to='organizations.organization')),
                ('to_organization', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='to_organization', to='organizations.organization')),
            ],
            options={
                'verbose_name': 'Organizations Connection',
                'ordering': ('-id',),
            },
        ),
    ]