# Generated by Django 4.0.3 on 2022-04-08 10:15

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ap_News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Content_Pitching', 'Content_Pitching'), ('Writing_Rewrite', 'Writing_Rewrite'), ('Review_Draft_1', 'Review_Draft_1'), ('Review_Draft_2', 'Review_Draft_2'), ('FDN_Approval_1', 'FDN_Approval_1'), ('Ready_For_Release', 'Ready_For_Release'), ('App_Published', 'App_Published')], default='APNews_Content_Pitching', max_length=30)),
                ('published_on', models.DateField(blank=True, null=True)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('reverted_count', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'AP-News',
            },
        ),
        migrations.CreateModel(
            name='Ap_Wire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Content_Pitching', 'Content_Pitching'), ('Writing_Rewrite', 'Writing_Rewrite'), ('Review_Draft_1', 'Review_Draft_1'), ('Review_Draft_2', 'Review_Draft_2'), ('FDN_Approval_1', 'FDN_Approval_1'), ('Ready_For_Release', 'Ready_For_Release'), ('App_Published', 'App_Published')], default='APWire_Content_Pitching', max_length=30)),
                ('published_on', models.DateField(blank=True, null=True)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('reverted_count', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'AP-Wire',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Content_Pitching', 'Content_Pitching'), ('Writing_Rewrite', 'Writing_Rewrite'), ('Review_Draft_1', 'Review_Draft_1'), ('Review_Draft_2', 'Review_Draft_2'), ('FDN_Approval_1', 'FDN_Approval_1'), ('Ready_For_Release', 'Ready_For_Release'), ('App_Published', 'App_Published')], max_length=20)),
                ('create', models.BooleanField(default=False)),
                ('edit', models.BooleanField(default=False)),
                ('view', models.BooleanField(default=False)),
                ('move', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('to_delete', models.BooleanField(default=False, verbose_name='delete')),
                ('Permission_Name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Permissions',
            },
        ),
        migrations.DeleteModel(
            name='apews_FDNApproval',
        ),
        migrations.DeleteModel(
            name='apnews_APPublished',
        ),
        migrations.DeleteModel(
            name='apnews_ContentPitching',
        ),
        migrations.DeleteModel(
            name='apnews_ReadyForRelease',
        ),
        migrations.DeleteModel(
            name='apnews_ReviewDraft1',
        ),
        migrations.DeleteModel(
            name='apnews_ReviewDraft2',
        ),
        migrations.DeleteModel(
            name='apnews_WritingRewrite',
        ),
        migrations.DeleteModel(
            name='apwire_APPublished',
        ),
        migrations.DeleteModel(
            name='apwire_ContentPitching',
        ),
        migrations.DeleteModel(
            name='apwire_FDNApproval',
        ),
        migrations.DeleteModel(
            name='apwire_ReadyForRelease',
        ),
        migrations.DeleteModel(
            name='apwire_ReviewDraft1',
        ),
        migrations.DeleteModel(
            name='apwire_ReviewDraft2',
        ),
        migrations.DeleteModel(
            name='apwire_WritingRewrite',
        ),
        migrations.RemoveField(
            model_name='usercustom',
            name='role',
        ),
        migrations.AlterField(
            model_name='usercustom',
            name='accessint',
            field=models.IntegerField(blank=True, default=7, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=7), django.core.validators.MinValueValidator(limit_value=1)]),
        ),
        migrations.AddField(
            model_name='permissions',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ap_wire',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ap_wire',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
        migrations.AddField(
            model_name='ap_news',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ap_news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]