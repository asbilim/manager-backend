# Generated by Django 4.2.1 on 2023-05-28 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('password_hashed', models.TextField(blank=True)),
                ('verify_hashed', models.CharField(blank=True, default='', max_length=255)),
                ('key', models.CharField(blank=True, max_length=200)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('passphrase', models.TextField()),
                ('link', models.URLField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('picture', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
