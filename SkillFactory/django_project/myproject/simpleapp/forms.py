from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductForm(forms.ModelForm):
   description = forms.CharField(min_length=20)
   class Meta:
       model = Product
       fields = [
           'name',
           'description',
           'quantity',
           'category',
           'price',
       ]

   def clean(self):
       cleaned_data = super().clean()
       description = cleaned_data.get("description")

       name = cleaned_data.get("name")
       if name == description:
           raise ValidationError({
               "name": "Описание не должно быть идентичным названию."
           })

       return cleaned_data