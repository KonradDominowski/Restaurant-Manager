# Generated by Django 4.0.4 on 2022-05-09 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('Przystawka', 'Przystawka'), ('Zupa', 'Zupa'), ('Danie główne', 'Danie główne'), ('Deser', 'Deser')], max_length=32)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ExtraInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vegetarian', models.BooleanField()),
                ('vegan', models.BooleanField()),
                ('celiac', models.BooleanField()),
                ('peanut_allergy', models.BooleanField()),
                ('dairy', models.BooleanField()),
                ('child_seat', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('prepared', models.BooleanField()),
                ('price', models.FloatField()),
                ('active', models.BooleanField()),
                ('dishes', models.ManyToManyField(to='manager_app.dish')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('guest_number', models.PositiveIntegerField()),
                ('date_hour', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReservationExtraInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.extrainfo')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.reservation')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='extra_info',
            field=models.ManyToManyField(through='manager_app.ReservationExtraInfo', to='manager_app.extrainfo'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.menu'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_app.table'),
        ),
    ]
