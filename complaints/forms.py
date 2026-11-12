from django import forms
from .models import Complaint, ComplaintUpdate


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            'title',
            'category',
            'location',
            'description',
            'photo'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AssignComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            'department',
            'admin_remarks'
        ]


class ComplaintUpdateForm(forms.ModelForm):

   class Meta:
        model = ComplaintUpdate

        fields = [
            'status',
            'remarks',
            'evidence_photo'
        ]

        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4}),
        }

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['status'].choices = [
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ]
