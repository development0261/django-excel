# Generated by Django 3.2.14 on 2022-08-03 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_usercustom_ap_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ap_news',
            name='category',
        ),
    ]
