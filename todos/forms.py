from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?',
                'class': 'form-input',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Add a note (optional)',
                'class': 'form-textarea',
                'rows': 2,
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
