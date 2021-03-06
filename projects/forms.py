from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description', 'customer']
        widgets = {'description': forms.fields.TextInput(attrs={'placeholder': 'Enter description'}), 'start_date': forms.widgets.DateInput(attrs={'type': 'date'}), 'end_date': forms.widgets.DateInput(attrs={'type': 'date'})}


class CreateProjectForm(ProjectForm):
    pass


class UpdateProjectForm(ProjectForm):
    
    class Meta(ProjectForm.Meta):
        pass
