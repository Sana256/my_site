import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from projects.models import Project, List, Item, Action, WorkDay
User = get_user_model()


class ProjectModelTest(TestCase):


    def setUp(self):
        self.user = User.objects.create(username='Sanek', password='qwerty12345')
        self.project = Project.objects.create(developer=self.user, name='first project', description='first description')


    def test_str_method(self):
        self.assertEqual(str(self.project), 'first project')


    def test_date_default(self):
        self.assertEqual(self.project.start_date, datetime.date.today())
        self.assertEqual(self.project.end_date, datetime.date.today())


    def test_project_ordering(self):
        end_date1 = datetime.date.today() + datetime.timedelta(days=2)
        project1 = Project.objects.create(developer=self.user, name='second project', description='description22', end_date=end_date1)
        end_date2 = datetime.date.today() + datetime.timedelta(days=-2)
        project2 = Project.objects.create(developer=self.user, name='third project', description='description33', end_date=end_date2)
        self.assertEqual(list(Project.objects.all()), [project1, self.project, project2])
