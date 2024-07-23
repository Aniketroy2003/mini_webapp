from django.urls import path, include
from .views import home, user_signup, user_login, user_logout,add_task,delete_task,edit_task, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('signup/', user_signup, name='signup'),

    path('add/', add_task, name='add_task'),
    path('edit/<int:todo_id>/', edit_task, name='edit_task'),
    path('delete/<int:todo_id>/', delete_task, name='delete_task'),
    path('profile/', profile, name='profile'),

]
