from django import forms
from Cart.models import Variation
from PIL import Image

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields  = '__all__'
        
