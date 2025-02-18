from django import forms
from localflavor.pl import forms
from .models import Customer

class UserForm(forms.ModelForm):
    
    class Meta:
        model = Customer
