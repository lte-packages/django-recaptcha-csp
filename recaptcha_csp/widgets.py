"""
CSP-aware ReCaptcha widgets.
"""

from captcha.widgets import ReCaptchaBase

from recaptcha_csp.context import get_csp_nonce


class CSPReCaptchaV2Checkbox(ReCaptchaBase):
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

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Try to get from widget attribute first (for backward compatibility)
        # then fall back to context storage
        context["csp_nonce"] = getattr(self, "csp_nonce", None) or get_csp_nonce()
        return context


class CSPReCaptchaV2Invisible(ReCaptchaBase):
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

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Try to get from widget attribute first (for backward compatibility)
        # then fall back to context storage
        context["csp_nonce"] = getattr(self, "csp_nonce", None) or get_csp_nonce()
        return context
