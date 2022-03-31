# Generated by Django 4.0.3 on 2022-03-30 09:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_blog_updated_blog2_updated_alter_blog_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercustom',
            name='accessint',
            field=models.IntegerField(blank=True, default=7, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=7), django.core.validators.MinValueValidator(limit_value=1)]),
        ),
    ]