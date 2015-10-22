
import base64
import hashlib
import logging

from allaccess.views import OAuthCallback

from allaccess.compat import smart_bytes, force_text
from allaccess.compat import get_user_model
from allaccess.clients import get_client
from allaccess.compat import smart_bytes, force_text
from allaccess.compat import get_user_model
from allaccess.models import Provider, AccountAccess

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect,render
from django.views.generic import RedirectView, View
from django.http import HttpResponseRedirect
from django.shortcuts import render


from inout.models import InoutUser,InoutUserLink
from inout.forms import InoutUserForm

from django.contrib.auth.decorators import login_required

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def Index(request):
    user=request.user
    if user.is_superuser:
        return HttpResponseRedirect('/admin/')
    if user.id==None:
        return render(request,'inout/index.html',{'user':None,'app_status':False})
    try:
        profile_links=user.inoutuser.inoutuserlink
    except InoutUserLink.DoesNotExist:
        return HttpResponseRedirect('/accounts/profile/')
    inout_user_status=user.inoutuser.application_status
    return render(request,'inout/index.html',{'user':request.user,'app_status':inout_user_status})

@xframe_options_exempt
def closed(request):
        return render(request,'inout/closed.html')

@xframe_options_exempt
@login_required
def UserDash(request):
    user=request.user
    if user.is_superuser:
        return HttpResponseRedirect('/admin/')
    inout_user=user.inoutuser
    if request.method == 'POST':
        form = InoutUserForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            user_links=form.save(commit=False)
            user_links.inout_user=inout_user
            user_links.save()
            return HttpResponseRedirect('/')
    else:
        try:
            profile_links=user.inoutuser.inoutuserlink
            return HttpResponseRedirect('/')
        except InoutUserLink.DoesNotExist:
            pass
        form = InoutUserForm()

    return render(request,'inout/dashboard.html',{'user':request.user,'inout_user':inout_user,'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class CustomCallback(OAuthCallback):

    def get(self, request, *args, **kwargs):
        name = kwargs.get('provider', '')
        try:
            provider = Provider.objects.get(name=name)
        except Provider.DoesNotExist:
            raise Http404('Unknown OAuth provider.')
        else:
            if not provider.enabled():
                raise Http404('Provider %s is not enabled.' % name)
            client = self.get_client(provider)
            callback = self.get_callback_url(provider)
            # Fetch access token
            raw_token = client.get_access_token(self.request, callback=callback)
            if raw_token is None:
                return self.handle_login_failure(provider, "Could not retrieve token.")
            # Fetch profile info
            info = client.get_profile_info(raw_token)
            try:
                info=info['data']
            except KeyError:
                pass
            if info is None:
                return self.handle_login_failure(provider, "Could not retrieve profile.")
            identifier = self.get_user_id(provider, info)

            if identifier is None:
                return self.handle_login_failure(provider, "Could not determine id.")
            # Get or create access record
            defaults = {
                'access_token': raw_token,
            }
            access, created = AccountAccess.objects.get_or_create(
                provider=provider, identifier=identifier, defaults=defaults
            )
            if not created:
                access.access_token = raw_token
                AccountAccess.objects.filter(pk=access.pk).update(**defaults)
            user = authenticate(provider=provider, identifier=identifier)
            if user is None:
                return self.handle_new_user(provider, access, info)
            else:
                return self.handle_existing_user(provider, user, access, info)

    def handle_existing_user(self, provider, user, access, info):
        "Login user and redirect."

        kwargs = {
            'school':info.pop('school')['name']
        }
        info.pop('id')
        info.pop('created_at')
        info.pop('updated_at')
        info.pop('email')
        kwargs.update(info)
        inout_user=InoutUser.objects.filter(participant=user.id).update(**kwargs)

        login(self.request, user)
        return redirect(self.get_login_redirect(provider, user, access))

    def get_or_create_user(self, provider, access, info):
        "Registrations Closed"
        return redirect('closed')
        "Create InOut user profile."
        '''kwargs = {
            'school':info.pop('school')['name']
        }
        info.pop('id')
        info.pop('created_at')
        info.pop('updated_at')
        email=info.pop('email')
        kwargs.update(info)
        new=InoutUser(**kwargs)


        digest = hashlib.sha1(smart_bytes(access)).digest()
        # Base 64 encode to get below 30 characters
        # Removed padding characters
        username = force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
        User = get_user_model()
        kwargs = {
            User.USERNAME_FIELD: username,
            'password': None,
            'email':email


        }
        new_user=User.objects.create_user(**kwargs)
        new.participant = new_user
        new.save()
        return new_user'''
