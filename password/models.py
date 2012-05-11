from django.contrib.auth.models import Group, User
from django.db import models

from django_simple_aes_field.fields import AESField


class Password(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    passwd = AESField()
    user = models.ForeignKey(User, related_name='user_related')
    group = models.ManyToManyField(Group, blank=True, help_text='Deselect all groups to make password private.')

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.domain:
            if not self.domain.startswith('http://') and not self.domain.startswith('https://'):
                self.domain = 'http://' + self.domain
        super(Password, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def is_public(obj):
        if obj.group.count() > 0:
            return True
        return False

    is_public.short_description = 'Public?'
    is_public.boolean = True

