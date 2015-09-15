from django import forms

from inout.models import InoutUserLink

class InoutUserForm(forms.ModelForm):
    class Meta:
        model = InoutUserLink
        exclude = ['inout_user']
        help_texts = {
            'additional_info': _('Briefly describe about your past achievements,projects,hacks etc. Also provide links to any other public profiles you have.'),
        }
