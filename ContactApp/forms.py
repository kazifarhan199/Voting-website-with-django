from .models import ContactModel
from django import forms

class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactModel
		exclude = []