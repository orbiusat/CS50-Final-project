# Generated by Django 4.1.3 on 2023-02-13 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0002_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='owner',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to=settings.AUTH_USER_MODEL),
        ),
    ]
