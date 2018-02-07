from django.urls import path

from projects import views

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects_view'),
    path('<int:pk>/', views.DetailProjectView.as_view(), name='detail_project_view'),
]
