from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.SignUpView.as_view(), name='registration'),
    path('profile/edit/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('logout/', views.custom_logout, name='logout'),
]
