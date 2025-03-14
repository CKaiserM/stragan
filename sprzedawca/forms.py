from django import forms
from .models import CompanyProfile
from localflavor.pl.forms import PLNIPField, PLPostalCodeField, PLProvinceSelect, PLCountySelect, PLREGONField

class CompanyInfoForm(forms.ModelForm):
    company_email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres E-Mail'}), required=False)
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer telefonu'}), required=True)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    house_and_street_no = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica i numer'}), required=True)
    postal_code = PLPostalCodeField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kod pocztowy'}), required=True)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kraj'}), required=True)
    company_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwa Firmy'}), required=True)
    company_logo = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}), required=False)
    nip = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'NIP'}), required=True)
    regon = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'REGON'}), required=True)

    class Meta:
        model = CompanyProfile
        fields = ('company_name', 'company_logo', 'company_email', 'nip', 'regon', 'phone', 'city', 'house_and_street_no', 'postal_code', 'country')
