from django import forms

from projects.models import Project


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description', 'customer']
