from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from projects.forms import CreateProjectForm, UpdateProjectForm
from projects.models import Project
User = get_user_model()

def home(request):
    return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class ProjectsView(ListView):
    '''display all project for current user'''

    template_name = 'projects_view.html'
    context_object_name = 'projects'

    def get_queryset(self):
        developer = self.request.user
        return Project.objects.filter(developer=developer)


@method_decorator(login_required, name='dispatch')
class DetailProjectView(DetailView):
    '''display project overview for current user'''

    model = Project
    template_name = 'detail_project_view.html'
    context_object_name = 'project'


    def get_queryset(self):
        developer = self.request.user
        return Project.objects.filter(developer=developer)


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = CreateProjectForm
    template_name = 'project_add.html'

    def form_valid(self, form):
        form.instance.developer = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = UpdateProjectForm
    template_name = 'project_update.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(developer=self.request.user)
