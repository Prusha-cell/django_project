from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Task_Manager'

    def ready(self):
        import Task_Manager.signals  # Импорт сигналов при старте приложения
