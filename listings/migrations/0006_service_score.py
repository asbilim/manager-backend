# Generated by Django 4.2.1 on 2023-06-04 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_alter_service_service_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
