from django import forms
from .models import user
from django.contrib.auth.forms import AuthenticationForm

class UserSignupForm(forms.ModelForm):
    # name = forms.CharField(label='Name', max_length=100)
    # email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    #role = forms.ChoiceField(choices=user.ROLE_CHOICES) 
    class Meta:
        model = user
        fields = ['Name', 'Role','Password']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class UserSigninForm(AuthenticationForm):
    class Meta:
        model = user
        fields = ['Name', 'Password']
