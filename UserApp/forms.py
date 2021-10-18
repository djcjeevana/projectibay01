from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import fields
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth import authenticate
from Location.models import *

#class PersonForm(UserCreationForm):

#class PersonForm(UserCreationForm):
#    #username = forms.CharField( label="User Name", widget=forms.TextInput(
#    #    attrs={'placeholder': 'Enter Your User Name'}))
#    
#    first_name = forms.CharField( label="First Name", widget=forms.TextInput(
#        attrs={'placeholder': 'Enter Your User Name'}))
#    last_name = forms.CharField( label="Last Name", widget=forms.TextInput(
#        attrs={'placeholder': 'Enter Your User Name'}))
#    email = forms.CharField( label="Email", widget=forms.EmailInput(
#        attrs={'placeholder': 'Enter Your Email '}))
#    
#    
#    
#    class Meta:
#        model = Person
#        fields = ( 'first_name', 'last_name', 'email', 'phone','country', 'city', 'vanue','address','password1','password2') # You Can Change This order
#        
#        
#        
#    def clean(self):
#        print("your are herererererewrewrwerewr")
#        cleaned_data = super(PersonForm, self).clean()
#        password = cleaned_data.get("password")
#        confirm_password = cleaned_data.get("password2")
#        if password != confirm_password:
#            raise forms.ValidationError(
#                "password and confirm_password does not match"
#        )
#            
#            
#    
#    def clean_email(self):
#        username = self.cleaned_data.get('name')
#        email = self.cleaned_data.get('email')
#        if email and Person.objects.filter(email=email).exclude(name=username).count():
#            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#        return email
#    
#    
#
#    def clean_name(self): # this name shoud be eques to data base filde
#        username = self.cleaned_data.get('name')
#        email = self.cleaned_data.get('email')
#        if username and Person.objects.filter(name=username).exclude(email=email).count():
#            raise forms.ValidationError('This username is already in use. Please supply a different username.')
#        return username
#        
#        
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#
#        self.fields['city'].queryset = District.objects.none()
#
#        
#
#        if 'country' in self.data:
#            try:
#                country_id = int(self.data.get('country'))
#                self.fields['city'].queryset = District.objects.filter(country_id=country_id).order_by('name')
#            except (ValueError, TypeError):
#                pass  # invalid input from the client; ignore and fallback to empty City queryset
#        elif self.instance.pk:
#            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
#
#        self.fields['vanue'].queryset = District.objects.none()
#        if 'city' in self.data:
#            try:
#                city_id = int(self.data.get('city'))
#                self.fields['vanue'].queryset = SubDistrict.objects.filter(district_id=city_id).order_by('name')
#            except (ValueError, TypeError):
#                pass  # invalid input from the client; ignore and fallback to empty City queryset
#        elif self.instance.pk:
#            #self.fields['vanue'].queryset = self.instance.country.city.vanue_set.order_by('name')
#            self.fields['vanue'].queryset = self.instance.city.vanue_set.order_by('name')
#
#
#
#class CustomerLoginForm(forms.Form):
#    username = forms.CharField(widget=forms.TextInput())
#    password = forms.CharField(widget=forms.PasswordInput())
#    
#    #email = forms.EmailField( label='Email', widget=forms.EmailInput(
#    #    attrs={'placeholder': 'Enter Your email'}))  
#    #password = forms.CharField( label="Password", widget=forms.PasswordInput(
#    #    attrs={'placeholder': 'Enter Your Password'}))
#    
    
    ############################################################################
#class NewUserForm(UserCreationForm):
#    email = forms.EmailField(required=True)
#    
#    class Meta:
#        model = User
#        fields = ("username", "email", "password1", "password2")
#    def save(self, commit=True):
#        user = super(NewUserForm, self).save(commit=False)
#        user.email = self.cleaned_data['email']
#        if commit:
#            user.save()
#        return user


        
        
        
class RegistrationForm(UserCreationForm):
   
    
    username = forms.CharField(max_length=100, label="username", widget=forms.TextInput(
        attrs={'placeholder': 'Write Your username', }))
    email = forms.EmailField(max_length=200, label='email', widget=forms.EmailInput(
        attrs={'placeholder': 'Write Your email'}))
    first_name = forms.CharField(max_length=100, label="first_name", widget=forms.TextInput(
        attrs={'placeholder': 'Write Your first name'}))
    last_name = forms.CharField(max_length=100, label="last_name", widget=forms.TextInput(
        attrs={'placeholder': 'Write Your last name'}))
    

    class Meta:
        model = UserBase
        fields = ('username', 'email',
                  'first_name','last_name','password1','password2')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = UserBase.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username
    
    

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})



class UserLoginForm(forms.ModelForm):
    
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    
    class Meta:
        model = UserBase
        fields = ('email','password')
        
    def clean(self):
        if self.is_valid():            
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Login")
        
        
        
class AccountUpdateForm(forms.ModelForm):
    
    
    username = forms.CharField(label='User Name',widget=forms.TextInput)
    first_name = forms.CharField(label='First Name',widget=forms.TextInput)
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput)
    phone_number = forms.CharField(label='Phone Number',widget=forms.TextInput)   
    postcode = forms.CharField(label='Postel Code',widget=forms.TextInput)
    address_line_1 = forms.CharField(label='Address',widget=forms.TextInput)
    town_city = forms.CharField(label='Password',widget=forms.TextInput)
    
      
    class Meta:
        model = UserBase
        fields = ('username','first_name','last_name','phone_number','postcode','address_line_1','town_city')
        
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = UserBase.objects.exclude(pk=self.instance.pk).get(username=username) #check this account is exist or not
            except UserBase.DoesNotExist:
                # if email is not there
                return username
            raise forms.ValidationError('UserName "%s" is already in user'  % account)
                
    
    def update_first_name(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            UserBase.objects.exclude(pk=self.instance.pk).get(first_name=first_name) #check this account is exist or not
            
        
    def update_last_name(self):
        if self.is_valid():
            last_name = self.cleaned_data['last_name']
            UserBase.objects.exclude(pk=self.instance.pk).get(last_name=last_name) #check this account is exist or not
            
        
          
        
    def update_phone_number(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            UserBase.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number) #check this account is exist or not
            
        
    def update_postcode(self):
        if self.is_valid():
            postcode = self.cleaned_data['postcode']
            UserBase.objects.exclude(pk=self.instance.pk).get(postcode=postcode) #check this account is exist or not
            
        
    def update_address_line_1(self):
        if self.is_valid():
            address_line_1 = self.cleaned_data['address_line_1']
            UserBase.objects.exclude(pk=self.instance.pk).get(address_line_1=address_line_1) #check this account is exist or not
            
    def update_town_city(self):
        if self.is_valid():
            town_city = self.cleaned_data['town_city']
            UserBase.objects.exclude(pk=self.instance.pk).get(town_city=town_city) #check this account is exist or not
            
         