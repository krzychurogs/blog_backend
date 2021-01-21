from entries.models import Entries
from django.forms import ModelForm
from django import forms


INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]
class EntryForm(forms.ModelForm):
	
	class Meta:
		model=Entries
		fields=('entry_title','entry_text','image')
		labels = {
			'entry_title': 'Tytuł',
			'entry_text': 'Tekst',
			'image': 'Obrazek',
			

		}
