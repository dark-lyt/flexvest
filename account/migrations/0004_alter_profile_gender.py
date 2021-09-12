# Generated by Django 3.2.6 on 2021-09-09 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('', 'Others'), ('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
