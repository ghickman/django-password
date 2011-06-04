from django.contrib import admin
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from forms import PasswordForm
from models import Password

class UserGroupsFilterSpec(RelatedFilterSpec):
    """
    Custom filter spec taken from:
    http://stackoverflow.com/questions/2251851/django-admin-list-filter-attribute-from-userprofile
    """
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(UserGroupsFilterSpec, self).__init__(f, request, params, model, model_admin, field_path=field_path)

        # The lookup string that will be added to the queryset by this filter
        self.lookup_kwarg = 'group__id__exact'
        # get the current filter value from GET (we will use it to know which filter item is selected)
        self.lookup_val = request.GET.get(self.lookup_kwarg)

        # A list of the user's groups, ordered alphabetically, containing only the id and name.
        self.lookup_choices = Group.objects.filter(user=request.user).order_by('name').values_list('id', 'name')

    def choices(self, cl):
        """
        Generator that returns all the possible items in the filter including 'All' and 'Private' items.
        """
        yield { 'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All') }
        for pk_val, val in self.lookup_choices:
            yield { 'selected' : self.lookup_val == smart_unicode(pk_val),
                    'query_string': cl.get_query_string({self.lookup_kwarg: pk_val}),
                    'display': val }

    def title(self):
        return _('Group')

# Here, we insert the new FilterSpec at the first position, to be sure it gets picked up before any other.
FilterSpec.filter_specs.insert(0,
    (lambda f: getattr(f, 'usergroup_filter', False), UserGroupsFilterSpec)
)

# Add the usergroup filter by setting the usergroup_filter attribute on an existing field.
# This will activate the user groups filter if we add it to the admin's `list_filter`,
# however we won't be able to use it in it's own filter anymore.
Password._meta.get_field('group').usergroup_filter = True

class PasswordAdmin(admin.ModelAdmin):
    form = PasswordForm
    list_display = ('__unicode__', 'domain', 'is_public')
    list_filter = ('group',)
    search_fields = ['name', 'username', 'domain']

    def get_form(self, request, obj=None, **kwargs):
         form = super(PasswordAdmin, self).get_form(request, obj, **kwargs)
         form.current_user = request.user
         return form

    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(PasswordAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(Q(user=user) | Q(group=Group.objects.filter(user=user))).distinct()

admin.site.register(Password, PasswordAdmin)

