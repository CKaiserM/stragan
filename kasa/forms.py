from django import forms
from .models import ShippingAddress, InvoiceDetails
from localflavor.pl.forms import PLNIPField, PLPostalCodeField, PLProvinceSelect, PLCountySelect

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię i nazwisko'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres E-Mail'}), required=False)
    shipping_city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    shipping_house_and_street_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica'}), required=True)
    shipping_postal_code = PLPostalCodeField()


    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_house_and_street_no', 'shipping_city', 'shipping_postal_code']

        exclude = ['user',]   

class InvoiceForm(forms.ModelForm):
    company_nip = PLNIPField()
    company_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwa firmy'}), required=True)
    company_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres E-Mail'}), required=True)
    company_city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    company_house_and_street_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica i numer'}), required=True)
    company_postal_code = PLPostalCodeField()


    class Meta:
        model = InvoiceDetails
        fields = ['company_full_name', 'company_email', 'company_house_and_street_no', 'company_city', 'company_postal_code', 'company_province', 'company_voivodeship']

        exclude = ['user',]   

