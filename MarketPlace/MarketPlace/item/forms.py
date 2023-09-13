from django import forms
from .models import Item

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category','name','description','price','quantity','image',)

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name','description','price','quantity','image',)
        
