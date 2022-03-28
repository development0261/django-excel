# Generated by Django 4.0.3 on 2022-03-28 07:28

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_blog_publishedon_alter_blog2_publishedon'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='blog2',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='blog2',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]