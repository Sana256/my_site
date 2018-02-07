from django.test import TestCase

from django.contrib.auth import login, get_user_model
User = get_user_model()

from projects.models import Project


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Sanek', password='qwerty12345')
        self.user2 = User.objects.create_user(username='Vanek', password='ewq321')

        self.project1 = Project.objects.create(developer=self.user, name='first project', description='first description')
        self.project2 = Project.objects.create(developer=self.user, name='second project', description='second description')
        self.project3 = Project.objects.create(developer=self.user2, name='third project', description='blabla')


class HomeViewTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ProjectsViewTest(TestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get('/projects/')


    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_uses_projects_view_template(self):
        self.assertTemplateUsed(self.response, 'projects_view.html')


class ProjectsViewTest(ViewsTest):

    def setUp(self):
        super().setUp()
        self.client.login(username='Sanek', password='qwerty12345')
        self.response = self.client.get(f'/projects/')


    def test_user_is_login(self):
        self.assertTrue(self.response.context['user'].is_authenticated)


    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_uses_user_projects_view_template(self):
        self.assertTemplateUsed(self.response, 'projects_view.html')


    def test_dispay_only_login_user_project(self):
        self.assertContains(self.response, 'first project')
        self.assertContains(self.response, 'second project')
        self.assertNotContains(self.response, 'third project')

    def test_logout_users_redirects(self):
        self.client.logout()
        response = self.client.get('/projects/')
        self.assertRedirects(response, '/accounts/login?next=/projects/', target_status_code=301)

class ProjectViewTest(ViewsTest):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(f'/projects/{self.project1.id}/')

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_template(self):
        self.assertTemplateUsed(self.response, 'detail_project_view.html')
