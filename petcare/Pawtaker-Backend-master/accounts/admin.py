from django.contrib import admin
from .models import CustomUser, ResetPasswordLink

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parent_name",
        "phone_number",
        "email",
        "image",
        "address",
        "date_of_birth",
    )


admin.site.register(CustomUser, CustomUserAdmin)


class Resetlink(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "expired_at")


admin.site.register(ResetPasswordLink, Resetlink)
