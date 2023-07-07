from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
]
# path('update_profile/   ', views.update_profile, name='update_profile'),
