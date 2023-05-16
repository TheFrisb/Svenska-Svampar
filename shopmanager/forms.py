from django import forms
from shop.models import UserProfile

class ExportOrdersForm(forms.Form):
    date_from = forms.DateField(label = "Почетна дата", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label = "Крајна дата", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    user_profile = forms.ChoiceField(widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(ExportOrdersForm, self).__init__(*args, **kwargs)
        self.fields['user_profile'].choices = self.get_dynamic_choices()

    def get_dynamic_choices(self):
        choices = []
        user_profiles = UserProfile.objects.all()
        for profile in user_profiles:
            choice = (profile.id, profile.business_name)
            choices.append(choice)
        return choices