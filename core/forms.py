from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Model-backed contact form for the website contact page."""

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
                    'class': 'w-full bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)] px-4 py-3 rounded-lg border border-neutral-800 focus:border-[color:var(--color-accent-primary)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-accent-primary)]/20 transition',
                    'placeholder': 'Dimitri Gaggioli',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)] px-4 py-3 rounded-lg border border-neutral-800 focus:border-[color:var(--color-accent-primary)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-accent-primary)]/20 transition',
                    'placeholder': 'dimitri.gaggioli@gmail.com',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'w-full bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)] px-4 py-3 rounded-lg border border-neutral-800 focus:border-[color:var(--color-accent-primary)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-accent-primary)]/20 transition',
                    'placeholder': '+33 6 12 34 56 78 (optionnel)',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'w-full bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)] px-4 py-3 rounded-lg border border-neutral-800 focus:border-[color:var(--color-accent-primary)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-accent-primary)]/20 transition',
                    'placeholder': "Sujet de votre message",
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'w-full bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)] px-4 py-3 rounded-lg border border-neutral-800 focus:border-[color:var(--color-accent-primary)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-accent-primary)]/20 transition',
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


