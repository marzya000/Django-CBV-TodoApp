from .models import User
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('The password and its repetition do not match')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            return user
