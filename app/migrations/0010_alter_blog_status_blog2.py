# Generated by Django 4.0.3 on 2022-03-23 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_usercustom_appublished_usercustom_content_pitching_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('Content_Pitching', 'Content_Pitching'), ('Writing_Rewrite', 'Writing_Rewrite'), ('Review_Draft_1', 'Review_Draft_1'), ('Review_Draft_2', 'Review_Draft_2'), ('FDN_Approval_1', 'FDN_Approval_1'), ('Ready_For_Release', 'Ready_For_Release'), ('App_Published', 'App_Published')], default='APWire_Content_Pitching', max_length=30),
        ),
        migrations.CreateModel(
            name='Blog2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300)),
                ('image', models.ImageField(upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Content_Pitching', 'Content_Pitching'), ('Writing_Rewrite', 'Writing_Rewrite'), ('Review_Draft_1', 'Review_Draft_1'), ('Review_Draft_2', 'Review_Draft_2'), ('FDN_Approval_1', 'FDN_Approval_1'), ('Ready_For_Release', 'Ready_For_Release'), ('App_Published', 'App_Published')], default='APWire_Content_Pitching', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]