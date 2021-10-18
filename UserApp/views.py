from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from Stores.models import Setting
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout


#from orders.views import user_orders

from .forms import RegistrationForm,UserLoginForm,AccountUpdateForm
from .models import UserBase
from .tokens import account_activation_token

from urllib.parse import urlparse, urlunparse

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


@login_required
def dashboard(request):
    #orders = user_orders(request)
    
    return render(request,
                  'account/user/dashboard.html')
    

def register_request(request):
    
    
    if request.user.is_authenticated: # to check user is register or not
        return redirect('dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST) # To Rejester the user using post method me are taking data from the browser
        if registerForm.is_valid():#chek all the email password etc. are enderd correcctly . for that we use validation method.
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password1'])
            user.is_active = False # still user need make inactive. becaseu we need to check about him. becasue email activation is requered
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message) # in here you can add more informatino to your email. this your email body and content
            return HttpResponse('registered succesfully and activation sent')
        
    else:
        registerForm = RegistrationForm()
    setting = Setting.objects.get(id=1)
    context = {
               'setting': setting,
               'form': registerForm}
    
    return render(request, 'account/registration/register.html', context)

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # SUSPECT CODE 
        #current_user = request.user
        #data =UserBase()
        #data.id = current_user.id
        #data.profile_image="ibayimage/logo_1080_1080.png"
        #data.save()
        # SUSPECT CODE 
        return redirect('dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')



def homepage(request):
      return render(request, "index.html")

def registergmail(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f"New account created: {username}")
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    else:
      messages.error(request,"Account creation failed")

    return redirect("Stores:home")

  form = UserCreationForm()
  return render(request,"passwordreset/register.html", {"form": form})




def login_request(request):
    context = {}
    
    user = request.user
    if user.is_authenticated:
        return redirect("Stores:home")
    
    if request.POST: 
        form = UserLoginForm(request.POST)
        if form.is_valid():
             email = request.POST['email']
             password = request.POST['password']
             user = authenticate(request,email=email,password=password)
             
             if user:
                 login(request,user)
                 return redirect("Stores:home")
             
    else:
        form = UserLoginForm()
        
    setting = Setting.objects.get(id=1)
    context['setting'] = setting        
    context['login_form'] = form
    return render(request,'account/registration/login.html',context)



#def login_view(request):
#    context = {}
#    print("Your are hererererererewrewr")
#    
#    if request.POST:
#        print("Your are hererererererewrewr")
#        form = AuthenticationForm(request, data=request.POST)    
#        if form.is_valid():
#            print("your ind uner is valided")
#            email = form.cleaned_data.get('email')
#            print("emailllllll",email)
#            password = form.cleaned_data.get('password')
#            print("paswwwrodllllll",password)
#            user = authenticate(email=email, password=password)
#            if user is not None:
#                login(request, user)
#                messages.info(request, f"You are now logged in as {email}.")
#                print("you are good to gooo")
#                return redirect("Stores:home")
#
#             
#            else:
#                print("your are insde loging fail")
#                messages.error(request,"Invalid username or password.")
#             
#             
#        else:
#            print("your are innsde loging faiileeeee")
#            messages.error(request,"Invalid username or password.")
#            
#    form = AuthenticationForm()   
#    setting = Setting.objects.get(id=1)
#    context['setting'] = setting        
#    context['login_form'] = form
#    return render(request,'account/registration/login.html',context)



def logout_request(request):
    logout(request)
    return redirect("Stores:home")


def account_update(request):
    
    if not request.user.is_authenticated:
        return redirect("Stores:home")
    
    context = {}
    
    if request.POST:
        form = AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
        
    else:
        form = AccountUpdateForm(
                initial={
                 "username":request.user.username,
                 "first_name":request.user.first_name,
                 "last_name":request.user.last_name,
                 "phone_number":request.user.phone_number,
                 "postcode":request.user.postcode,
                 "address_line_1":request.user.address_line_1,
                 "town_city":request.user.town_city,
                    
                }
                )
    setting = Setting.objects.get(id=1)
    context['setting'] = setting
    context['account_form'] = form
    return render(request,'account/registration/account.html',context)


def userprofile(request):
    
    setting = Setting.objects.get(id=1)
    current_user = request.user
    profile = UserBase.objects.get(id=current_user.id)
    
    context = {
               'setting': setting,
               'profile': profile}
    return render(request, 'account/registration/user_profile.html', context)

############################## Pasword Reset #######################################

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context



class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'passwordreset/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'passwordreset/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'passwordreset/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'passwordreset/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'passwordreset/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if 'uidb64' not in kwargs or 'token' not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserBase._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context



class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'passwordreset/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    print("Yoiur are herererererewrwerwerwerwerewr")
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'passwordreset/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'passwordreset/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        