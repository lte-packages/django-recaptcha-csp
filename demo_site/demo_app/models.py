"""
Models for demo_app.

This is intentionally minimal - the demo focuses on form validation
with reCAPTCHA, not data persistence.
"""
from django.db import models


class ContactSubmission(models.Model):
    """
    Optional model to store contact form submissions.
    Not required for the reCAPTCHA demo.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
