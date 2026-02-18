from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-4",
                "placeholder": "Enter Task Title",
            }
        ),
        label="title",
    )

    class Meta:
        model = Task
        fields = ["title"]
