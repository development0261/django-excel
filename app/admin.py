from django.contrib import admin
from django.apps import apps

from app.models import Blog, UserCustom,Blog2
from django.contrib.auth.admin import UserAdmin

# app = apps.get_app_config('app')

# for model_name, model in app.models.items():
#     admin.site.register(model)



class customuseradmin(UserAdmin):
     fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'Content_Pitching',
                    'Writing_Rewrite',
                    'ReviewDraft1',
                    'ReviewDraft2',
                    'FDNApproval',
                    'ReadyForRelease',
                    'APPublished',
                    'accessint'

                    
                ),
            },
        ),
    )

admin.site.register(UserCustom,customuseradmin)

@admin.register(Blog)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")

@admin.register(Blog2)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")