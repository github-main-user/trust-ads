from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "role",
        "image",
        "is_active",
    )
    list_filter = ("role", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "role", "phone", "image")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password", "password2")}),
    )
