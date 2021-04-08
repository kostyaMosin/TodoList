from django.urls import path

from .views import view_create_task_and_todo_list, view_edit_task,\
    view_delete_task, view_sort_by_priority, view_complete_task, view_move_rating_task

urlpatterns = [
    path('', view_create_task_and_todo_list, name='index'),
    path('edit/<int:pk>', view_edit_task, name='edit'),
    path('delete/<int:pk>', view_delete_task, name='delete'),
    path('move/<int:pk>', view_move_rating_task, name='move'),
    path('sort/<priority>', view_sort_by_priority, name='sort'),
    path('complete/<int:pk>', view_complete_task, name='complete'),
]
