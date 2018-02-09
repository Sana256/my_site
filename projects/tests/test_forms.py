from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from projects.forms import ProjectForm, CreateProjectForm, UpdateProjectForm
from projects.models import Project


class FormsTest(TestCase):
    '''basic setup'''
    def setUp(self):
        self.user = User.objects.create_user(username='Sanek', password='qwerty12345')


class ProjectFormTest(FormsTest):

    def test_form_save(self):
        form = ProjectForm(data={'name':'project name', 'description': 'project description'})
        project = form.save()
        self.assertEqual(project, Project.objects.first())


    def test_validation_for_blank_name(self):
        form = ProjectForm(data={'name':'', 'description': 'project description'})
        self.assertFalse(form.is_valid())



class CreateProjectFormTest(FormsTest):
    pass


class UpdateProjectFormTest(FormsTest):
    pass
