from django import forms
from .models import CompanyProfile
from localflavor.pl.forms import PLNIPField, PLPostalCodeField, PLProvinceSelect, PLCountySelect, PLREGONField
from rynek.models import Product, ProductImages, Subcategory

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

class MultipleImagesInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    

class MultipleImagesField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImagesInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial = None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    
class MultipleImagesFieldForm(forms.Form):
    file_field = MultipleImagesField()

class AddProductForm(forms.ModelForm):

    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwa produktu'}), required=True)
    price = forms.DecimalField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cena'}), required=True)
    unit = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Jednostka miary'}), required=True)
    category = forms.ModelChoiceField(queryset=Subcategory.objects.all(), label="", widget=forms.Select(attrs={'class':'form-select'}), required=True)
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Opis'}), required=True)
    featured_image = forms.ImageField(label="", widget=forms.FileInput(attrs={"class":"form-control"}), required=True)
    status = forms.BooleanField(required=False)
    quantity = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ilość'}), required=True)
    
    class Meta:
        model = Product
        fields = ('title', 'price', 'unit', 'category', 'description', 'featured_image', 'status', 'quantity')
        exclude = ["user"]
        
class AddProductImagesForm(forms.ModelForm):

    image = MultipleImagesField(label="", widget=MultipleImagesInput(attrs={'class':'form-control'}), required=False)
    
    class Meta:
        model = ProductImages
        fields = ('image',)    