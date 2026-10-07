from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('todo/', views.to_do, name='todo'),
    path('todo/update/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('todo/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('todo/toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
]