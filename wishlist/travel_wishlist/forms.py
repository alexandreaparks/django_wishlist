from django import forms
from .models import Place


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place  # create form relating to Place model
        fields = ('name', 'visited')  # include the name and visited fields on form
