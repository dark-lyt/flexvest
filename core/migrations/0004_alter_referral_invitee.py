# Generated by Django 3.2.6 on 2021-09-09 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20210904_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee', to=settings.AUTH_USER_MODEL),
        ),
    ]
