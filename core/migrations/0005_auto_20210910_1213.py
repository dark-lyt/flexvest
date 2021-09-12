# Generated by Django 3.2.6 on 2021-09-10 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_alter_referral_invitee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='user',
        ),
        migrations.RemoveField(
            model_name='selectplan',
            name='payed_date',
        ),
        migrations.AlterField(
            model_name='referral',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
