from django.urls import path
from . import views

urlpatterns = [
        path('manage/<int:project_id>/', views.manage_ticket, name='manage_ticket'),
        path('create_ticket/<int:project_id>/', views.create_ticket, name='create_ticket'),
]
