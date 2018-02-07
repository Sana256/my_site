from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from projects.models import Project
User = get_user_model()

def home(request):
    return render(request, 'home.html')

@method_decorator(login_required, name='dispatch')
class ProjectsView(ListView):

    template_name = 'projects_view.html'
    context_object_name = 'projects'

    def get_queryset(self):
        developer = self.request.user
        return Project.objects.filter(developer=developer)


class DetailProjectView(DetailView):

    model = Project
    template_name = 'detail_project_view.html'
    context_object_name = 'project'


    def get_queryset(self):
        developer = self.request.user
        return Project.objects.filter(developer=developer)
