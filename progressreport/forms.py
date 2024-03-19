from django import forms
from .models import ProgressReportRequest

class ProgressReportRequestForm(forms.ModelForm):
    class Meta:
        model = ProgressReportRequest
        fields = ['subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Message'})
