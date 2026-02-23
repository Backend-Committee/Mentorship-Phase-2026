from django.contrib.auth.forms import UserCreationForm
import django.forms.fields as fields
from .models import Profile
import zoneinfo

TIMEZONES = [(timezone, timezone) for timezone in zoneinfo.available_timezones()]
TIMEZONES.sort()

class ProfileCreationForm(UserCreationForm):
    timezone = fields.ChoiceField(choices=TIMEZONES, required=True)
    
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super().save(commit) 
        user_profile = Profile(user=user, timezone=self.cleaned_data['timezone'])
        user_profile.save()
        return user_profile