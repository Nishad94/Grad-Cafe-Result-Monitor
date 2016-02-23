from django.contrib import admin
from .models import resultItem, gcUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(resultItem)
admin.site.register(gcUser)

# Define an inline admin descriptor for gcUser model
# which acts a bit like a singleton
class gcUserInline(admin.StackedInline):
    model = gcUser
    can_delete = False
    verbose_name_plural = 'gradCafeUser'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (gcUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)