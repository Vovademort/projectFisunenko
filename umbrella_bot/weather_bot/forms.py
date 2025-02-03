from django import forms
from .models import UserSettings

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['chat_id', 'city', 'notification_time']
        widgets = {
            'notification_time': forms.TimeInput(attrs={'type': 'time'}),
        }