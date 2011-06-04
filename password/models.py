from base64 import b64decode

from django.contrib.auth.models import Group, User
from django.db import models

class Password(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    passwd = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='incunapassword_employee_related')
    group = models.ManyToManyField(Group, help_text='Deselect all groups to make password private.')

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.domain:
            if not self.domain.startswith('http://') and not self.domain.startswith('https://'):
                self.domain = 'http://' + self.domain
        super(Password, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def password(self):
        return b64decode(self.passwd)

    def is_public(obj):
        if obj.group.count() > 0:
            return True
        else:
            return False
    is_public.short_description = 'Public?'
    is_public.boolean = True

