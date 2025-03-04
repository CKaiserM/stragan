from django import forms
from .models import ShippingAddress, InvoiceDetails
from localflavor.pl.forms import PLNIPField, PLPostalCodeField, PLProvinceSelect, PLCountySelect

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię i nazwisko'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres E-Mail'}), required=True)
    shipping_city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    shipping_street = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica'}), required=True)
    shipping_house_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer domu'}), required=True)
    shipping_flat_number = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer mieszkania'}), required=False)
    shipping_postal_code = PLPostalCodeField()
    shipping_province = PLProvinceSelect()
    shipping_voivodeship = PLCountySelect()

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_street', 'shipping_house_number', 'shipping_flat_number', 'shipping_city', 'shipping_postal_code', 'shipping_province', 'shipping_voivodeship']

        exclude = ['user',]   

class InvoiceForm(forms.ModelForm):
    company_nip = PLNIPField()
    company_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwa firmy'}), required=True)
    company_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres E-Mail'}), required=True)
    company_city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miasto'}), required=True)
    company_street = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulica'}), required=True)
    company_house_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer domu'}), required=True)
    company_flat_number = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer mieszkania'}), required=False)
    company_postal_code = PLPostalCodeField()
    company_province = PLProvinceSelect()
    company_voivodeship = PLCountySelect()

    class Meta:
        model = InvoiceDetails
        fields = ['company_full_name', 'company_email', 'company_street', 'company_house_number', 'company_flat_number', 'company_city', 'company_postal_code', 'company_province', 'company_voivodeship']

        exclude = ['user',]   

