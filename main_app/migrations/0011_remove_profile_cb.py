# Generated by Django 3.0.8 on 2020-07-09 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20200708_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cb',
        ),
    ]
