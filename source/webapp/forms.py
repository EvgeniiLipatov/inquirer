from django import forms
from django.contrib.auth.models import User

from webapp.models import Product, Review

class ProductReviewsForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['good', 'text', 'mark']
