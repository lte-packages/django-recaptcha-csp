"""
Views for the demo app.
"""

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactFormCheckbox, ContactFormInvisible, SimpleForm


def index(request):
    """
    Home page with links to different demo pages.
    """
    return render(request, "demo_app/index.html")


def contact_checkbox(request):
    """
    Contact form view using CSP-aware reCAPTCHA v2 Checkbox.

    Demonstrates:
    - Standard visible checkbox reCAPTCHA
    - Automatic CSP nonce injection via middleware
    - No need to pass request to form constructor!
    """
    if request.method == "POST":
        # Notice: We don't need to pass the request to the form!
        # The middleware handles the CSP nonce automatically.
        form = ContactFormCheckbox(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # In a real app, you'd save to database or send email here
            messages.success(
                request,
                f"Thank you, {name}! Your message has been received. "
                f"(Verified with reCAPTCHA v2 Checkbox)",
            )
            return redirect("success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactFormCheckbox()

    return render(
        request,
        "demo_app/contact_checkbox.html",
        {
            "form": form,
            "form_title": "Contact Form (reCAPTCHA v2 Checkbox)",
        },
    )


def contact_invisible(request):
    """
    Contact form view using CSP-aware reCAPTCHA v2 Invisible.

    Demonstrates:
    - Invisible reCAPTCHA (validates on submit)
    - Automatic CSP nonce injection via middleware
    - Seamless user experience
    """
    if request.method == "POST":
        form = ContactFormInvisible(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            messages.success(
                request,
                f"Thank you, {name}! Your message has been received. "
                f"(Verified with reCAPTCHA v2 Invisible)",
            )
            return redirect("success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactFormInvisible()

    return render(
        request,
        "demo_app/contact_invisible.html",
        {
            "form": form,
            "form_title": "Contact Form (reCAPTCHA v2 Invisible)",
        },
    )


def simple_form(request):
    """
    Simple form without reCAPTCHA for comparison.
    """
    if request.method == "POST":
        form = SimpleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            messages.success(request, f"Thank you, {name}! (No reCAPTCHA on this form)")
            return redirect("success")
    else:
        form = SimpleForm()

    return render(
        request,
        "demo_app/simple_form.html",
        {
            "form": form,
            "form_title": "Simple Form (No reCAPTCHA)",
        },
    )


def success(request):
    """
    Success page shown after form submission.
    """
    return render(request, "demo_app/success.html")


def csp_info(request):
    """
    Page showing CSP information for educational purposes.
    """
    csp_nonce = getattr(request, "csp_nonce", None)

    return render(
        request,
        "demo_app/csp_info.html",
        {
            "csp_nonce": csp_nonce,
        },
    )
