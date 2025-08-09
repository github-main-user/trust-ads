from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "description", "author", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
