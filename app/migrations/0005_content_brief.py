# Generated by Django 4.0.3 on 2022-04-12 12:54

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_ap_news_published_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='content_brief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
            ],
        ),
    ]
