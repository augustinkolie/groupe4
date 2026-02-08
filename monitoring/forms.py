from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage, NewsletterSubscriber, Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'latitude', 'longitude', 'station_type', 'sensors_count', 'location_description', 'image', 'pollution_causes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'premium-control', 'placeholder': 'Nom de la station'}),
            'latitude': forms.NumberInput(attrs={'class': 'premium-control', 'placeholder': 'Ex: 9.5', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'premium-control', 'placeholder': 'Ex: -13.7', 'step': '0.000001'}),
            'station_type': forms.Select(attrs={'class': 'premium-control'}),
            'sensors_count': forms.NumberInput(attrs={'class': 'premium-control', 'placeholder': 'Nombre de capteurs'}),
            'location_description': forms.Textarea(attrs={'class': 'premium-control', 'placeholder': 'Description...', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'premium-control', 'accept': 'image/*'}),
            'pollution_causes': forms.Textarea(attrs={'class': 'premium-control', 'placeholder': 'Causes de la pollution...', 'rows': 3}),
        }

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
