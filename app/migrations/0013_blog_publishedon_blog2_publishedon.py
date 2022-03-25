# Generated by Django 4.0.3 on 2022-03-25 09:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_blog_description_alter_blog2_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publishedon',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog2',
            name='publishedon',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]