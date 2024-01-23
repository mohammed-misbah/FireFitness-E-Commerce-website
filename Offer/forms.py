from django import forms
from Offer.models import *
class ProductofferForm(forms.ModelForm):
    class Meta:
        model = Productoffer
        fields = '__all__'

class CategoryofferForm(forms.ModelForm):
    class Meta:
        model = Categoryoffer
        fields = '__all__'