# Generated by Django 4.1.2 on 2022-11-03 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_myuser_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
