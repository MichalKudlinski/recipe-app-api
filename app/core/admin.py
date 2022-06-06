from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext_lazy as _
# Register your models here.
"""Django admin customization"""

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ["email","name"]
    fieldsets=(('admin',{'fields':('email','password')}),(
        _('Permissions'),{
            'fields':('is_active','is_staff','is_superuser'
                      )
        }
         ),(_('Important dates'),{'fields':('last_login',)}),
               )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2','name','is_active','is_staff','is_superuser')
        }),
    )





admin.site.register(models.User,UserAdmin) #because we write in User admin it changes to our customized settings
admin.site.register(models.Recipe)