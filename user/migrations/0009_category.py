# Generated by Django 3.2.6 on 2023-09-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20230906_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rasm', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
