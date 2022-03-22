from django.contrib import admin
from django.apps import apps

from app.models import UserCustom
from django.contrib.auth.admin import UserAdmin

app = apps.get_app_config('app')

for model_name, model in app.models.items():
    admin.site.register(model)