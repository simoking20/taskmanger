
from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Tasks
    path('list/', views.task_list, name='task_list'),
    path('mine/', views.my_tasks, name='my_tasks'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.update_task, name='update_task'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('new/', views.create_task, name='create_task'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/update/', views.update_event, name='update_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
]

