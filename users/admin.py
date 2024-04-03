from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Роль пользователя в системе',
            {
                'fields': (
                    'is_customer', #роль начальников цеха
                    'is_manager', #роль менеджеров, персонала по обработке заявок
                    'is_admin', #роль модератора\админа для работы со всем содержимым медиа сайта
                    'is_boss', #роль начальников для отслеживания статистики выполнения работ и тд.
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
