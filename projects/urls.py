from django.urls import path
from . import views

urlpatterns = [
        path('create_project/', views.create_project, name='create_project'),
        path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
        path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),

]