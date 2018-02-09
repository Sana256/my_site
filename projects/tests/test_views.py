from django.test import TestCase

from django.contrib.auth import login, get_user_model
User = get_user_model()

from projects.models import Project
from projects.forms import CreateProjectForm


class ViewsTest(TestCase):
    '''basic setup'''
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


class ProjectsViewTest(ViewsTest):

    def setUp(self):
        super().setUp()
        self.client.login(username='Sanek', password='qwerty12345')
        self.response = self.client.get('/projects/')


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


class DetailProjectViewTest(ViewsTest):

    def setUp(self):
        super().setUp()
        self.client.login(username='Sanek', password='qwerty12345')
        self.response = self.client.get(f'/projects/{self.project1.id}/')


    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_uses_template(self):
        self.assertTemplateUsed(self.response, 'detail_project_view.html')


    def test_logout_users_redirects(self):
        self.client.logout()
        response = self.client.get(f'/projects/{self.project1.id}/')
        self.assertRedirects(response, f'/accounts/login?next=/projects/{self.project1.id}/', target_status_code=301)


    def test_dispay_only_login_current_user_projects(self):
        self.assertContains(self.response, 'first project')
        self.assertNotContains(self.response, 'third project')


    def test_not_display_projects_for_another_login_user(self):
        self.client.logout()
        self.client.login(username='Vanek', password='ewq321')
        response = self.client.get(f'/projects/{self.project1.id}/')
        self.assertEqual(response.status_code, 404)


class ProjectCreateViewTest(ViewsTest):

    def setUp(self):
        super().setUp()
        self.client.login(username='Sanek', password='qwerty12345')


    def test_can_save_post_request(self):
        response = self.client.post('/projects/add/', data={'name': 'new project name'})
        new_project = Project.objects.order_by('-pk')[0]
        self.assertEqual(new_project.name, 'new project name')
        self.assertEqual(Project.objects.count(), 4) #3 create on setup


    def test_redirect_after_post_date(self):
        response = self.client.post('/projects/add/', data={'name': 'new project name'})
        new_project = Project.objects.order_by('-pk')[0]
        self.assertRedirects(response, f'/projects/{new_project.id}/')


    def test_invalid_inputs_renders_add_project_template(self):
        response = self.client.post('/projects/add/', data={'name': ''})
        self.assertTemplateUsed(response, 'project_add.html')
        self.assertIsInstance(response.context['form'], CreateProjectForm)


    def test_invalis_inputs_dont_save(self):
        response = self.client.post('/projects/add/', data={'name': ''})
        new_project = Project.objects.order_by('-pk')[0]
        self.assertEqual(Project.objects.count(), 3) # 3 objects create on setup
