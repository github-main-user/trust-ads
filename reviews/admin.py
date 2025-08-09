from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "ad", "created_at")
    list_filter = ("author", "ad")
    search_fields = ("text",)
    ordering = ("created_at",)
    readonly_fields = ("created_at",)
