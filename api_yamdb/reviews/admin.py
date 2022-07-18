from django.contrib import admin

from .models import Comment, Review

admin.site.register(Comment)
admin.site.register(Review)
