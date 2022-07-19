from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Class to customize Users display in admin panel."""
    list_display = [
        'pk', 'username', 'email', 'role', 'first_name', 'last_name', 'bio']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['role']
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
