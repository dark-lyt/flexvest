from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from django.forms import widgets
from django.forms.widgets import PasswordInput, RadioSelect
from django_countries import countries
from django_countries.fields import Country, CountryField, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile
from core.models import Plan


GENDER_CHOICES = (
    ('', "Others"),
    ('M', 'Male'),
    ('F', 'Female')
)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput)
    remember_me = forms.BooleanField()

# REGISTRATION CLASS widget=forms.CheckboxInput(attrs={'class': 'checkbox checkbox-login-v1 keep'})


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20, min_length=8, widget=forms.TextInput(
        attrs={'class': 'register_input register-form-border', }))

    country = forms.ChoiceField(widget=CountrySelectWidget(attrs={'class': 'form-control', 'style': 'width:100%;', 'onkeyup': 'restrict(&#39;email&#39;)'},
                                                           layout='{widget}<img class="country-select-flag"  \
                                                           id="{flag_id}" style="margin: 0px 0px 0px 0px; width:30px; height:30px" src="{country.flag}">'), choices=countries)
    phone_number = PhoneNumberField()

    gender = forms.ChoiceField(widget=RadioSelect(
        attrs={'class': 'register-form-border'}), choices=GENDER_CHOICES)

    zip_postal = forms.CharField(required=True, max_length=6, widget=forms.TextInput())

    select_plan = forms.ModelMultipleChoiceField(queryset=Plan.objects.all(
    ), widget=forms.SelectMultiple(attrs={'class': 'register-form-border', 'style': 'width:100%;'}))

    password = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


# Enable users edit profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-group form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-group form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-group form-control'})
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('country', 'phone_number', 'gender')
        widgets = {
            'gender': forms.RadioSelect(attrs={"class": "uniform-inline"}),
            'country': CountrySelectWidget(attrs={'class': 'form-group form-control col-6'},
                                           layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 0px 0px 0px 0px; width:30px; height:30px" src="{country.flag}">'),
            'phone_number': PhoneNumberField.hidden_widget(attrs={'class': 'form-group form-control'})


        }
