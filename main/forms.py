from django import forms
from .models import Feedback


class CropSearchForm(forms.Form):
    crop = forms.CharField(
        label="Price of ",
        max_length=100,
        widget=forms.TextInput(attrs=
                               {"id": "crop",
                                "class": "autocomplete-input",
                                "autocomplete": "off",
                                "placeholder": "e.g. Carrots"
                                }))
    

class Compare(forms.Form):
    crop1 = forms.CharField( label="Compare", 
                            max_length=100, 
                            widget=forms.TextInput(attrs=
                                                   {"id": "crop",
                                                    "class": "autocomplete-input",
                                                    "autocomplete": "off",
                                                    "placeholder": "e.g. Carrot"}))
    crop2 = forms.CharField( label="to", 
                            max_length=100, 
                            widget=forms.TextInput(attrs=
                                                   {"id": "crop2",
                                                    "class": "autocomplete-input",
                                                    "autocomplete": "off",
                                                    "placeholder": "e.g. Tomato"}))
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message']