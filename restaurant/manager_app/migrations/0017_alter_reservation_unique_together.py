# Generated by Django 4.0.4 on 2022-06-07 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0016_reservation_end_hour'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set(),
        ),
    ]
