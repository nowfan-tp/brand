from django import forms

from .models import *

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields =['coupon_code','discount','is_active']
        widgets = {
            'coupon_code' :forms.TextInput(attrs={'class':'form-contrl'}),
            'discount' :forms.TextInput(attrs={'class':'form-contrl'}),

        }