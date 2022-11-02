# Generated by Django 4.1.2 on 2022-10-31 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_myuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.RegexValidator('(84|0[3|5|7|8|9])+([0-9]{8})\\b', message='Enter valid phone number')]),
        ),
    ]
