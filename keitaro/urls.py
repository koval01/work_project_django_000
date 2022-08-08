from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user, name="create_user"),
    path('login/', views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    path('home/', views.home, name="home")
]
