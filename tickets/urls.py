from django.urls import path
from . import views

urlpatterns = [
        path('manage/', views.manage_ticket, name='manage_ticket'),
        path('create_ticket/', views.create_ticket, name='create_ticket'),
        path('create_ticket/<int:project_id>/', views.create_ticket, name='create_ticket'),
        path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
        path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
        path('edit_ticket/', views.edit_ticket, name='edit_ticket'),
        path('see_ticket/', views.user_manage_ticket, name='user_ticket_dashboard'),
        path('update_status/<int:ticket_id>/', views.update_status, name='user_update_status'),
        path('see_notification/', views.get_notification, name='get_notifications'),
]
