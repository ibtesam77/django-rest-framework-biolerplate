from django.contrib import admin

from ..models import TemporaryToken


class TemporaryTokenAdmin(admin.ModelAdmin):
    model = TemporaryToken
    list_display = ('user', 'key', 'expiry_time')
    list_display_links = None
    search_fields = ('user',)

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(TemporaryToken, TemporaryTokenAdmin)
