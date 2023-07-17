# Generated by Django 4.0.4 on 2023-07-08 16:41

from django.db import migrations, models
import django.db.models.deletion
import manager_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0021_alter_reservation_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='restaurant',
            field=models.ForeignKey(default=manager_app.models.Restaurant.get_default_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.restaurant', verbose_name='Restauracja'),
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(default=manager_app.models.Restaurant.get_default_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.restaurant', verbose_name='Restauracja'),
        ),
        migrations.AddField(
            model_name='table',
            name='restaurant',
            field=models.ForeignKey(default=manager_app.models.Restaurant.get_default_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.restaurant', verbose_name='Restauracja'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='restaurant',
            field=models.ForeignKey(default=manager_app.models.Restaurant.get_default_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.restaurant', verbose_name='Restauracja'),
        ),
    ]