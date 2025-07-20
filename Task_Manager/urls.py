from django.urls import path
from .views import (TaskListCreateView,
                    TaskDetailUpdateDeleteView,
                    SubTaskListCreateView,
                    SubTaskDetailUpdateDeleteView,
                   # task_create,
                   # task_list,
                   # task_detail,
                   display_statistic_tasks, )
# from Task_Manager.views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    # path('tasks/create/', task_create, name='task-create'),  # Маршрут для создания новой задачи
    # path('tasks/', task_list, name='task-list'),  # Маршрут для получения всех задач
    # path('tasks/<int:pk>/', task_detail, name='task-detail'),  # Маршрут для получения одной задачи
    path('tasks/statistic/', display_statistic_tasks, name='task-statistic'),  # Маршрут для получения статистики задач
    # path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),  # Маршрут для получения списка и создания подзадач
    # path('subtasks/<int:pk>',
    #      SubTaskDetailUpdateDeleteView.as_view(),
    #      name='subtask-detail-update-delete'),  # Маршрут для получения конкретной подзадачи, обновления, удаления подзадачи
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail-update-delete'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtasks-detail-update-delete')
]
