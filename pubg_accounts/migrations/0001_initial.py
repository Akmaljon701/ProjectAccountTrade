# Generated by Django 3.2.6 on 2023-09-06 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PUBG MOBILE Global', 'PUBG MOBILE Global'), ('PUBG MOBILE Lite', 'PUBG MOBILE Lite'), ('PUBG MOBILE Korean', 'PUBG MOBILE Korean'), ('PUBG MOBILE India', 'PUBG MOBILE India'), ('PUBG (PC)', 'PUBG (PC)')], max_length=50)),
                ('level', models.CharField(max_length=10)),
                ('rp', models.CharField(max_length=255)),
                ('clothes', models.CharField(max_length=255)),
                ('skins', models.CharField(max_length=255)),
                ('titles', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('confirmed', models.BooleanField(default=False)),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('account_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pubg_accounts.account')),
            ],
        ),
    ]
