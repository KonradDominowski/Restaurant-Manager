# Generated by Django 4.0.4 on 2022-09-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0017_alter_reservation_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='prepared',
            field=models.BooleanField(default=True),
        ),
    ]
