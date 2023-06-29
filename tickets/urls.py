from django.urls import path
from . import views

urlpatterns = [
        path('create_ticket/<pk:project_id>/', views.create_ticket, name='create_ticket'),
]
