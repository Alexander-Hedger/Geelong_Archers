from django import forms

from .models import PageContent


class ContentForm(forms.ModelForm):
    class Meta:
        model = PageContent
        fields = {
            'content',
        }
