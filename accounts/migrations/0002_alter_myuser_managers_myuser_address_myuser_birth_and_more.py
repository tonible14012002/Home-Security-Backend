# Generated by Django 4.1.2 on 2022-10-31 09:21

import accounts.models
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
                ('is_admin', accounts.models.AdminUserManager()),
                ('is_ordinary', accounts.models.OrdinaryUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='address',
            field=models.CharField(default='ta quang buu', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='birth',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='myuser',
            name='phone',
            field=models.CharField(default='090232323', max_length=15, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.RegexValidator('/((^(\\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$/', message='Enter valid phone number')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='myuser',
            unique_together={('phone', 'email')},
        ),
    ]
