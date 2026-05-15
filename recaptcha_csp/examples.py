"""
Example usage of django-recaptcha-csp in a Django project.
"""

from captcha.fields import ReCaptchaField
from django import forms
from django.forms import ModelForm

from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox, CSPReCaptchaV2Invisible

# ============================================================================
# RECOMMENDED APPROACH: Using Middleware (No mixin required!)
# ============================================================================


# Example 1: Basic form with automatic CSP support
class ContactForm(forms.Form):
    """Simple contact form - no mixin needed with middleware!"""

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox)


# Example 2: ModelForm with automatic CSP support
class UserRegistrationForm(ModelForm):
    """ModelForm - no mixin needed with middleware!"""

    captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox)

    class Meta:
        # model = User  # Your model here
        fields = ["username", "email", "password"]


# Example 3: Using invisible reCAPTCHA
class NewsletterForm(forms.Form):
    """Newsletter form with invisible reCAPTCHA"""

    email = forms.EmailField()
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Invisible)


# Example view usage with middleware:
"""
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        # No need to pass request! Middleware handles it automatically
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form
            return redirect('success')
    else:
        # Just instantiate normally - that's it!
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
"""
