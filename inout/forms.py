from django import forms

from inout.models import InoutUserLinks

class InoutUserForm(forms.ModelForm):
    class Meta:
        model = InoutUserLinks
        exclude = ['inout_user']
