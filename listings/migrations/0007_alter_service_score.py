# Generated by Django 4.2.1 on 2023-06-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_service_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='score',
            field=models.IntegerField(blank=True, default=75, null=True),
        ),
    ]