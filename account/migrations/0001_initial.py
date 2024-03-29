# Generated by Django 3.2 on 2021-04-21 12:47

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('mobileNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
