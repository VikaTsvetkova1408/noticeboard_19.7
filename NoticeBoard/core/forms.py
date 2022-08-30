from django import forms
from allauth.account.forms import SignupForm
from .models import Notice, Rejoinder


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['category', 'content']

    def clean(self):
        super().clean()
        category = self.cleaned_data.get('category')
        if not category:
            self.add_error('category', 'No category selected!')


class RejoinderForm(forms.ModelForm):
    class Meta:
        model = Rejoinder
        fields = ['content']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        return user
