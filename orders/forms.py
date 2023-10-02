from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput
from .models import Order  # replace with your actual model import
import re


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'address': 'Endereço',
            'postal_code': 'CEP',
            'city': 'Cidade',
        }
        widgets = {
            'postal_code' : TextInput(attrs={'placeholder':'00000-000'}),
        }

    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        pattern = re.compile(r'^\d{5}-\d{3}$')
        
        if not pattern.fullmatch(data):  # Use fullmatch here
            raise ValidationError('Invalid postal code format. Use 00000-000.')

        return data