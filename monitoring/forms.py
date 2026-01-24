from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage, NewsletterSubscriber

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requis.')

    class Meta:
        model = User
        fields = ("username", "email")

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nom',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Sujet',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Votre message...',
                'rows': 5,
                'required': True
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Le message doit contenir au moins 10 caractères.")
        return message

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Votre email...',
                'required': True
            })
        }
