"""
Custom adapter for django-allauth to skip the intermediate signup page
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import User
from django.shortcuts import redirect


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to automatically create user accounts from social login
    without showing the intermediate signup form
    """
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Always allow auto signup - no intermediate page
        """
        return True
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user data from social account
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Get email from social account data
        email = data.get('email', '')
        if email:
            user.email = email
        
        # Generate username from email if not provided
        if not user.username:
            if email:
                # Use email prefix as username
                username_base = email.split('@')[0]
                username = username_base
                
                # Ensure username is unique
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{username_base}{counter}"
                    counter += 1
                
                user.username = username
            else:
                # Fallback: use social account UID
                user.username = f"user_{sociallogin.account.uid}"
        
        # Set first and last name if available
        if 'given_name' in data:
            user.first_name = data['given_name']
        if 'family_name' in data:
            user.last_name = data['family_name']
        
        return user
    
    def pre_social_login(self, request, sociallogin):
        """
        Connect existing user if email matches
        """
        # If user is already logged in, do nothing
        if request.user.is_authenticated:
            return
        
        # Try to connect to existing user with same email
        if sociallogin.is_existing:
            return
        
        try:
            email = sociallogin.account.extra_data.get('email', '').lower()
            if email:
                # Check if user with this email already exists
                user = User.objects.filter(email__iexact=email).first()
                if user:
                    # Connect this social account to the existing user
                    sociallogin.connect(request, user)
        except Exception:
            # If anything fails, just continue with normal flow
            pass
    
    def get_login_redirect_url(self, request):
        """
        Override to ensure redirect to dashboard after login
        """
        return '/dashboard/'
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save the user - called during signup
        """
        user = super().save_user(request, sociallogin, form)
        return user

