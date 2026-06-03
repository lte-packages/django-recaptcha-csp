"""
Forms demonstrating django-recaptcha-csp usage.
"""

from captcha.fields import ReCaptchaField
from django import forms

from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox, CSPReCaptchaV2Invisible


class ContactFormCheckbox(forms.Form):
    """
    Contact form with CSP-aware reCAPTCHA v2 Checkbox.

    This demonstrates the standard visible checkbox reCAPTCHA
    that works with Content Security Policy nonces.
    """

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your.email@example.com"}
        )
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject of your message"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your message...", "rows": 5}
        )
    )
    # CSP-aware reCAPTCHA v2 Checkbox widget
    # The middleware automatically provides the CSP nonce!
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox())


class ContactFormInvisible(forms.Form):
    """
    Contact form with CSP-aware reCAPTCHA v2 Invisible.

    This demonstrates the invisible reCAPTCHA that automatically
    validates when the form is submitted.
    """

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your.email@example.com"}
        )
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject of your message"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your message...", "rows": 5}
        )
    )
    # CSP-aware reCAPTCHA v2 Invisible widget
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Invisible())


class SimpleForm(forms.Form):
    """
    Simple form for basic testing without reCAPTCHA.
    """

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your.email@example.com"}
        )
    )
