# Generated by Django 3.2.6 on 2023-09-04 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20230904_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='verification_code',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
