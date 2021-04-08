from django import forms


CHOICES = (
    ('1', 'low'),
    ('2', 'medium'),
    ('3', 'high'),
)


class TaskForm(forms.Form):
    content = forms.CharField(max_length=255)
    priority = forms.ChoiceField(choices=CHOICES)
