# Generated by Django 3.2.14 on 2022-08-03 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_ap_news_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='ap_news',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]
