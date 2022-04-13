
from .models import category
from django.contrib import admin
from django.apps import apps

from app.models import Ap_Wire, UserCustom,Ap_News,permissions,content_brief
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)


# app = apps.get_app_config('app')

# for model_name, model in app.models.items():
#     admin.site.register(model)

@admin.register(content_brief)
class Display(admin.ModelAdmin):
    list_display = ('topic',)

class customuseradmin(UserAdmin):
     fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (

                    'accessint',

                    
                ),
            },
        ),
    )

# admin.site.register(UserCustom,customuseradmin)

@admin.register(UserCustom)
class UserProfileAdmin(UserAdmin):
    list_display = ['username','email','first_name','last_name','is_staff','is_superuser']

    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (

                    'accessint',

                    
                ),
            },
        ),
    )
# @admin.register(category)
# class BlogDisplay(admin.ModelAdmin):
#     pass

@admin.register(Ap_Wire)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")
    exclude = ('reverted_count',)

@admin.register(Ap_News)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")
    exclude = ('reverted_count',)

@admin.register(permissions)
class selectiondisplay(admin.ModelAdmin):
    list_display = ("status",'get_user_permission',"create","edit","view","move","publish","to_delete")

    def get_user_permission(self, obj):
        return " || ".join([p.username for p in obj.user.all()])


@admin.register(category)
class Display(admin.ModelAdmin):
    list_display = ("name", )



