# Generated by Django 4.0.3 on 2022-04-20 04:58

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCustom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('accessint', models.IntegerField(blank=True, default=7, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=7), django.core.validators.MinValueValidator(limit_value=1)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ap_News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Content_Pitching', 'Story Pitching'), ('Writing_Rewrite', 'Writing & Rewriting'), ('Review_Draft_1', 'First Review'), ('Review_Draft_2', 'Second Review'), ('FDN_Approval_1', 'Ready For FDN Approval'), ('Ready_For_Release', 'Ready For Release'), ('App_Published', 'AP Published')], default='APNews_Content_Pitching', max_length=30)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('reverted_count', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('status', models.CharField(choices=[('Content_Pitching', 'Story Pitching'), ('Writing_Rewrite', 'Writing & Rewriting'), ('Review_Draft_1', 'First Review'), ('Review_Draft_2', 'Second Review'), ('FDN_Approval_1', 'Ready For FDN Approval'), ('Ready_For_Release', 'Ready For Release'), ('App_Published', 'AP Published')], default='APWire_Content_Pitching', max_length=30)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('reverted_count', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'AP-Wire',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='content_brief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Content Brief',
            },
        ),
        migrations.CreateModel(
            name='permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Content_Pitching', 'Story Pitching'), ('Writing_Rewrite', 'Writing & Rewriting'), ('Review_Draft_1', 'First Review'), ('Review_Draft_2', 'Second Review'), ('FDN_Approval_1', 'Ready For FDN Approval'), ('Ready_For_Release', 'Ready For Release'), ('App_Published', 'AP Published')], max_length=20, unique=True)),
                ('create', models.BooleanField(default=False)),
                ('edit', models.BooleanField(default=False)),
                ('view', models.BooleanField(default=False)),
                ('move', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('to_delete', models.BooleanField(default=False, verbose_name='delete')),
                ('Permission_Name', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Permissions',
            },
        ),
        migrations.CreateModel(
            name='moreimages_apwire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.ap_wire')),
            ],
            options={
                'verbose_name_plural': 'AP-Wire Images',
            },
        ),
        migrations.CreateModel(
            name='moreimages_apnews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.ap_news')),
            ],
            options={
                'verbose_name_plural': 'AP-News Images',
            },
        ),
        migrations.AddField(
            model_name='ap_wire',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
        migrations.AddField(
            model_name='ap_news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]
