from django import forms

from inout.models import InoutUserLink

class InoutUserForm(forms.ModelForm):
    class Meta:
        model = InoutUserLink
        exclude = ['inout_user']
