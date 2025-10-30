from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Model-backed contact form for the website contact page."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'style': 'display:none;',
                'tabindex': '-1',
                'autocomplete': 'off',
            }
        ),
    )

    class Meta:
        model = ContactMessage
        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'message',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500/20 transition',
                    'placeholder': 'Dimitri Gaggioli',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500/20 transition',
                    'placeholder': 'dimitri.gaggioarruvéli@gmail.com',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500/20 transition',
                    'placeholder': '+33 6 12 34 56 78 (optionnel)',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500/20 transition',
                    'placeholder': "Sujet de votre message",
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500/20 transition',
                    'placeholder': 'Décrivez votre projet, vos besoins ou votre message...',
                    'rows': 6,
                }
            ),
        }

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message or "") < 20:
            raise forms.ValidationError("Le message doit contenir au moins 20 caractères.")
        return message

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('website'):
            raise forms.ValidationError("Spam détecté")
        return cleaned_data


