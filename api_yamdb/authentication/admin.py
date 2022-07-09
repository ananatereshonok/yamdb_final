from django.conf import settings as conf_settings
from django.contrib import admin
from django.contrib.auth import get_user_model

EMPTY_VALUE_DISPLAY = conf_settings.EMPTY_VALUE_DISPLAY

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи."""
    list_display = ('pk', 'username', 'email', 'role')
    search_fields = ('username', 'email')
    empty_value_display = EMPTY_VALUE_DISPLAY
