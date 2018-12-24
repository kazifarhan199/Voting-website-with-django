from django import forms
from .models import Options, Titles
from crispy_forms.helper import FormHelper

class OptionForm(forms.ModelForm):

	class Meta:
		model = Options
		fields = {
			'image',
			'cost', 
			'name', 
			'title',
			'detail1',
			'detail2',
			'detail3',
		}

class TitleForm(forms.ModelForm):
	class Meta:
		model = Titles
		fields = [
			'title',
			'published',
			'end',
		]
		helper = FormHelper()