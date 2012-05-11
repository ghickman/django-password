from django.contrib import admin

from .forms import PasswordForm
from .models import Password


class PasswordAdmin(admin.ModelAdmin):
    form = PasswordForm
    list_display = ('__unicode__', 'domain', 'is_public')
    list_filter = ('group',)
    search_fields = ['name', 'username', 'domain']

    def get_form(self, request, obj=None, **kwargs):
         form = super(PasswordAdmin, self).get_form(request, obj, **kwargs)
         form.current_user = request.user
         return form


admin.site.register(Password, PasswordAdmin)

