from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    versbose_name_plural = "Profiles"
    fields = ("phone", "address", "date_of_birth")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin panel for users"""

    inlines = (UserProfileInline,)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")

    # Поля для поиска
    search_fields = ("email", "first_name", "last_name")

    # Порядок сортировки
    ordering = ("email",)

    # Переопределяем fieldsets для формы редактирования
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
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

    # Поля для формы создания нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Фильтр по горизонтали для групп и разрешений
    filter_horizontal = ("groups", "user_permissions")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin panel for user profiles"""

    list_display = ("user", "phone", "date_of_birth", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "phone")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        ("Contact Information", {"fields": ("phone", "address")}),
        ("Personal Information", {"fields": ("date_of_birth",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
