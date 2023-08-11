from django.contrib import admin

from ..models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'is_active')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('is_active',)
    list_per_page = 25


admin.site.register(User, UserAdmin)
