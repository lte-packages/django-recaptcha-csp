"""
CSP-aware ReCaptcha widgets.
"""

from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV2Invisible

from recaptcha_csp.context import get_csp_nonce


class CSPNonceMixin:
    """
    Mixin to add CSP nonce support to ReCaptcha widgets.

    Injects the nonce from the request context into the widget context,
    allowing inline scripts to work with strict Content Security Policy.
    """

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Get nonce and add to context AFTER parent context is built
        nonce = get_csp_nonce()
        # Add to root context
        context["csp_nonce"] = nonce
        # Also try adding to widget attrs in case template looks there
        if "widget" in context and nonce:
            context["widget"]["csp_nonce"] = nonce
        return context


class CSPReCaptchaV2Checkbox(CSPNonceMixin, ReCaptchaV2Checkbox):
    """
    ReCaptcha V2 Checkbox widget with CSP nonce support.

    This widget extends the standard ReCaptchaV2Checkbox to include
    the CSP nonce in the widget context, allowing inline scripts to
    work with strict Content Security Policy.

    The nonce is automatically retrieved from the request context via
    middleware, so no manual passing is required.

    Usage:
        from captcha.fields import ReCaptchaField
        from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox

        class MyForm(forms.Form):
            captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox)

        # No need to pass request!
        form = MyForm()
    """

    template_name = "recaptcha_csp/widget_v2_checkbox.html"


class CSPReCaptchaV2Invisible(CSPNonceMixin, ReCaptchaV2Invisible):
    """
    ReCaptcha V2 Invisible widget with CSP nonce support.

    The nonce is automatically retrieved from the request context via
    middleware, so no manual passing is required.

    Usage:
        from captcha.fields import ReCaptchaField
        from recaptcha_csp.widgets import CSPReCaptchaV2Invisible

        class MyForm(forms.Form):
            captcha = ReCaptchaField(widget=CSPReCaptchaV2Invisible)

        # No need to pass request!
        form = MyForm()
    """

    template_name = "recaptcha_csp/widget_v2_invisible.html"
