from django.urls import path
from . import views

app_name = 'app_desk'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:task_id>', views.task_detail, name='task_detail'),
    path('add_task', views.task_add, name='task_add'),
    path('status_update', views.status_update, name='status_update')
]

