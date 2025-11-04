from django import forms
from .models import Task, Event
from django.contrib.auth import get_user_model

User = get_user_model()
class TaskForm(forms.ModelForm):
    """
    Form to create and update Task instances.
    Excludes 'created_by' as it will be set automatically in the view.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'document', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only regular users (not staff or superusers)
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=False, is_superuser=False)

class EventForm(forms.ModelForm):
    """
    Form to create and update Event instances.
    Excludes 'created_by' as it will be set automatically in the view.
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
