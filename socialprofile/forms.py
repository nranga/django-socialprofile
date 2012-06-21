"""Django forms for the socialprofile application"""
from django import forms
from django.contrib.auth.models import User
from models import SocialProfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import strip_tags
from django.forms.models import model_to_dict
from widgets import H5EmailInput
import logging

logger = logging.getLogger(name='socialprofile')

class SocialProfileForm(forms.Form):
    """Master form for editing the user's profile"""
    username = forms.CharField(max_length=30, label='User Name')
    email = forms.EmailField(label="Email Address", widget=H5EmailInput())
    first_name = forms.CharField(max_length=30, required=False, label='First Name',)
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    gender = forms.CharField(max_length=10, required=False, widget=forms.Select(choices=SocialProfile.GENDER_CHOICES))
    url = forms.URLField(required=False, label='Homepage URL', widget=forms.TextInput(attrs={'size': '100', }))
    image_url = forms.URLField(required=False, label='Profile Picture URL', widget=forms.TextInput(attrs={'size': '100', }))
    description = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'rows':'1', 'cols':'80'}))

    def clean_username(self):
        """Automatically called by Django, this method 'cleans' the username, which means making sure it's unique"""
        working_username = self.cleaned_data.get('username')

        # Check Username for Uniqueness
        try:
            existingUser = User.objects.get(username=working_username)
        except ObjectDoesNotExist:
            existingUser = None
        if existingUser is not None and self.user is not None:
            if self.user.id != existingUser.id:
                self._errors['username'] = self.error_class([u"Your new username is not unique!"])

        return working_username

    def clean_description(self):
        """Strip HTML out of description"""
        return strip_tags(self.cleaned_data['description'])

    def __init__(self, data=None, user=None, initial=None, *args, **kwargs):
        """Lets you pass in a user= to bind this form from"""
        self.user = user
        if initial is None and isinstance(user, User):
            initial = model_to_dict(user) # Set initial values for form to user object properties
            initial.update( model_to_dict(user.social_profile)) # Add User Profile properties to initial values
        super(SocialProfileForm, self).__init__(data=data, initial=initial)
