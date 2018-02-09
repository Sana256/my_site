from django.urls import path

from projects import views

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects_view'),
    path('<int:pk>/', views.DetailProjectView.as_view(), name='detail_project_view'),
    path('add/',views.ProjectCreateView.as_view(), name='project_add'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
]
