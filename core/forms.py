from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Model-backed contact form with honeypot spam protection.

    Note: Consider using django-honeypot for more robust spam protection.
    """

    # Honeypot field (should remain empty)
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "style": "display:none;",
                "tabindex": "-1",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]

        # Use form template instead of inline classes
        # Create core/templates/core/forms/contact_form.html with proper styling
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Dimitri Gaggioli",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "dimitri.gaggioli@gmail.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "+33 6 12 34 56 78 (optionnel)",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Sujet de votre message",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "placeholder": "Décrivez votre projet, vos besoins ou votre message...",
                    "rows": 6,
                }
            ),
        }

    def clean(self):
        """Validate honeypot field to prevent spam."""
        cleaned_data = super().clean()

        # Honeypot check
        if cleaned_data.get("website"):
            raise forms.ValidationError("Spam détecté")

        return cleaned_data
