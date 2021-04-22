from django import forms


CHOICES = (
    ('1', 'low'),
    ('2', 'medium'),
    ('3', 'high'),
)


class TaskForm(forms.Form):
    content = forms.CharField(max_length=255, required=False)
    priority = forms.ChoiceField(choices=CHOICES, required=False)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Content field is empty')
        return content
