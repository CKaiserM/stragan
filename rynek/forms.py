from django import forms
from .models import Customer, Profile, Address
from localflavor.pl.forms import PLNIPField, PLPostalCodeField, PLProvinceSelect, PLCountySelect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer telefonu'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    house_and_street_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica i numer'}), required=True)
    postal_code = PLPostalCodeField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kod pocztowy'}), required=True)


    class Meta:
        model = Profile
        fields = ('phone', 'city', 'house_and_street_no', 'postal_code')



# Sign-Up form

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres Email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Twoje hasło nie może być zbyt podobne do Twoich danych osobowych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Hasło nie może być powszechnie używanym hasłem.</li><li>Hasło nie może składać się wyłącznie z cyfr.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Potwierdź hasło'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>W celu weryfikacji, wprowadź ponownie hasło</small></span>'

# Update user form

class UpdateUserForm(UserChangeForm):

    password = None
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Wymagane. 150 znaków lub mniej. Tylko litery, cyfry i @/./+/-/_.</small></span>'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['first_name'].label = ''

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['last_name'].label = ''
