from django import forms
from .models import Notice, Rejoinder


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['category', 'content']


class RejoinderForm(forms.ModelForm):
    class Meta:
        model = Rejoinder
        fields = ['content']
