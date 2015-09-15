from django import forms

from inout.models import InoutUserLink

class InoutUserForm(forms.ModelForm):
    class Meta:
        model = InoutUserLink
        exclude = ['inout_user']
        widgets = {
            'additional_info': Textarea(attrs={'placeholder':"'Briefly describe about your past achievements,projects,hacks etc. Also provide links to any other public profiles you have.'"}),
        }
