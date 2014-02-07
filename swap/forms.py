from django import forms

from models import Item, SeedType

#User registration forms
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
    fullname = forms.CharField(max_length=40)
    address = forms.CharField(max_length=40)
    region = forms.CharField(max_length=40)
    interests = forms.CharField(max_length=60)

#Seed Item form
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('inventory',)

#Seed SeedType form
class SeedTypeForm(forms.ModelForm):
    class Meta:
        model = SeedType
        exclude = ('verified',)

#Basic Search form
class SearchForm(forms.Form):
    """Search posts by keyword"""
    name = forms.CharField(max_length=100, required=False)
    sci_name = forms.CharField(max_length=100, required=False)
    region = forms.CharField(max_length=100, required=False)
