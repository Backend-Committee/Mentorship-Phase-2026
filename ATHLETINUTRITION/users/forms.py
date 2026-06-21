from django import forms
from .models import AthleteProfile

class AthleteProfileForm(forms.ModelForm):
    class Meta:
        model = AthleteProfile
        fields = ['weight_kg', 'height_cm', 'sport_type', 'weekly_calorie_goal', 'weekly_protein_goal']