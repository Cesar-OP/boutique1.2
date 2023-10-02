from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 9)]


class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        max_quantity = kwargs.pop('max_quantity', 9)  # default to 9 if max_quantity is not provided
        super().__init__(*args, **kwargs)
        
        self.fields['quantity'] = forms.TypedChoiceField(
            label='Quantidade',
            choices=[(i, str(i)) for i in range(1, max_quantity + 1)],
            coerce=int
        )
    
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
