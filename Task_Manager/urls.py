from django.urls import path
from .views import task_create, task_list, task_detail, display_statistic_tasks

urlpatterns = [
    path('tasks/create/', task_create, name='task-create'),  # Маршрут для создания новой задачи
    path('tasks/', task_list, name='task-list'),  # Маршрут для получения всех задач
    path('tasks/<int:pk>/', task_detail, name='task-detail'),  # Маршрут для получения одной задачи
    path('tasks/statistic/', display_statistic_tasks, name='task-statistic')  # Маршрут для получения статистики задач
]
