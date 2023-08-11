from django.contrib import admin

from ..models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'is_active')
    readonly_fields = ('password', )
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('is_active',)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('user_permissions', 'is_admin', 'is_superuser')
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(User, UserAdmin)
