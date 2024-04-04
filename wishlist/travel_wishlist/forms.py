from django import forms
from .models import Place


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place  # create form relating to Place model
        fields = ('name', 'visited')  # include the name and visited fields on form


class DateInput(forms.DateInput):  # customize date input field - normally would be a text field
    input_type = 'date'


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }
