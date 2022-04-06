from django.contrib import admin
from django.apps import apps

from app.models import Ap_Wire, UserCustom,Ap_News,permissions
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


@admin.register(Ap_Wire)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")

@admin.register(Ap_News)
class BlogDisplay(admin.ModelAdmin):
    list_display = ("topic", "author","date","status")

@admin.register(permissions)
class selectiondisplay(admin.ModelAdmin):
    list_display = ("status",'get_user_permission',"create","edit","view","move","publish","to_delete")

    def get_user_permission(self, obj):
        return " || ".join([p.username for p in obj.user.all()])