from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    """Class to customize Categories display in admin panel."""
    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']


class GenreAdmin(admin.ModelAdmin):
    """Class to customize Genres display in admin panel."""
    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']


class TitleAdmin(admin.ModelAdmin):
    """Class to customize Titles display in admin panel."""
    list_display = ['pk', 'name', 'year', 'description', 'category']
    search_fields = ['name', 'description']
    list_filter = ['name', 'year', 'genre', 'category']
    empty_value_display = '-empty-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
