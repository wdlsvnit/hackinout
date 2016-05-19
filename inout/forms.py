from django import forms

from inout.models import InoutUserLink, Team, Participant

class InoutUserForm(forms.ModelForm):
    class Meta:
        model = InoutUserLink
        exclude = ['inout_user']
        widgets = {
            'additional_info': forms.Textarea(attrs={'placeholder':"Briefly describe about your past achievements, projects, hacks etc. Also provide links to any other public profiles you have."}),
        }
        labels = {
            'github_account': 'GitHub',
            'linkedin_account': 'LinkedIn',
        }
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['url_id','registration_date','application_status']
        labels = {
        'name':"Team Name",
        'email': "Team email",
        }
        error_messages = {
        'name' : {'max_length':"Team name can be maximum 30 characters.",},
        }
class ParticipantForm(forms.ModelForm):
    class Meta:
         model = Participant
         exclude = ['registration_date','team']
         widgets = {
            'graduation':forms.TextInput(attrs={'type':'date'}),
            'date_of_birth':forms.TextInput(attrs={'type':'date'}),
            'dietary_restrictions': forms.Textarea(attrs={'placeholder':"Please mention if you have any food related restrictions."}),
            'special_needs': forms.Textarea(attrs={'placeholder':"Please mention if you have any special requirements."}),
            'additional_info': forms.Textarea(attrs={'placeholder':"Briefly describe about your past achievements, projects, hacks etc. Also provide links to any other public profiles you have."}),
        }
        