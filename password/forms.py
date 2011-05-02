from base64 import b64encode

from django.forms import CharField, ModelForm

from models import Password

class PasswordForm(ModelForm):
    password = CharField(max_length=255)

    class Meta:
        model = Password
        exclude = ('user', 'passwd',)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.initial['password'] = self.instance.password
        #TODO Hide public field on the form when user doesn't own password
        #if self.instance.user != self.current_user:
            #del self.fields['is_public']
            #self.fields['is_public'].widget.attrs['disabled'] = True

    def save(self, commit=False):
        instance = super(PasswordForm, self).save(commit=False)
        instance.passwd = b64encode(self.cleaned_data['password'])
        if not instance.pk:
            instance.user = self.current_user
        instance.save()
        return instance

    def save_m2m(self):
        pass

