# Generated by Django 4.0.3 on 2022-03-22 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_apews_fdnapproval_apnews_appublished_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300)),
                ('image', models.ImageField(upload_to='')),
                ('type', models.CharField(choices=[('APWire_Content_Pitching', 'APWire_Content_Pitching'), ('APWire_Writing_Rewrite', 'APWire_Writing_Rewrite'), ('apwire_ReviewDraft1', 'apwire_ReviewDraft1'), ('apwire_ReviewDraft2', 'apwire_ReviewDraft2'), ('FDNApproval', 'FDNApproval'), ('ReadyForRelease', 'ReadyForRelease'), ('APPublished', 'APPublished')], default='APWire_Content_Pitching', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
        migrations.DeleteModel(
            name='UserTableConnection',
        ),
    ]