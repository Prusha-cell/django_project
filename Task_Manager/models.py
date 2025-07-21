from django.db import models
from django.utils import timezone

from Task_Manager.managers import SoftDeleteManager

# Статусы задачи
STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category name")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """Переопределяем стандартный метод удаления."""
        self.is_deleted = True  # Устанавливаем флаг
        self.deleted_at = timezone.now()
        self.save()  # Сохраняем изменения

    def restore(self):
        """Метод для восстановления записи."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [models.UniqueConstraint(fields=['name'], name='uniq_name')]


class Task(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Title")
    description = models.TextField(blank=True, verbose_name="Description")
    categories = models.ManyToManyField(Category, related_name="tasks", verbose_name="Categories")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    deadline = models.DateTimeField(verbose_name="Deadline")
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [models.UniqueConstraint(fields=['title'], name='uniq_title_task')]


class SubTask(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title subtask")
    description = models.TextField(blank=True, verbose_name="Description")
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE,
                             verbose_name="The main task")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    deadline = models.DateTimeField(verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.title} (to task: {self.task.title})"

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [models.UniqueConstraint(fields=['title'], name='uniq_title_subtask')]




####################### HOMEWORK_10 ####################################

# # Создание записей:
# # Task:
# # title: "Prepare presentation".
# # description: "Prepare materials and slides for the presentation".
# # status: "New".
# # deadline: Today's date + 3 days.
#
# new_task = Task.objects.create(title="Prepare presentation",
#                                description="Prepare materials and slides for the presentation",
#                                status="new",
#                                deadline=timezone.now() + timedelta(days=3))
#
# # SubTasks для "Prepare presentation":
# # title: "Gather information".
# # description: "Find necessary information for the presentation".
# # status: "New".
# # deadline: Today's date + 2 days.
# # title: "Create slides".
# # description: "Create presentation slides".
# # status: "New".
# # deadline: Today's date + 1 day.
#
# new_subtask = SubTask.objects.create(
#     task=new_task,
#     title="Gather information",
#     description="Find necessary information for the presentation",
#     status="new",
#     deadline=timezone.now() + timedelta(days=2)
# )
#
# new_subtask_2 = SubTask.objects.create(
#     task=new_task,
#     title="Create slides",
#     description="Create presentation slides",
#     status="new",
#     deadline=timezone.now() + timedelta(days=1)
# )
#
#
#
# # Tasks со статусом "New":
# # Вывести все задачи, у которых статус "New".
#
# tasks_new = Task.objects.filter(status='new')
# for task in tasks_new:
#     print(task)
#
#
# # SubTasks с просроченным статусом "Done":
# # Вывести все подзадачи, у которых статус "Done", но срок выполнения истек
#
# from django.db.models import Q
# done = SubTask.objects.filter(Q(status='done') & Q(deadline__lt=timezone.now()))
#
# # # Измените статус "Prepare presentation" на "In progress".
# new_task.status = 'in_progress'
# new_task.save()
#
# # Измените срок выполнения для "Gather information" на два дня назад.
# subtask = SubTask.objects.get(title="Gather information")
# subtask.deadline = timezone.now() - timedelta(days=2)
# subtask.save()
#
#
# # Измените описание для "Create slides" на "Create and format presentation slides".
# subtask_2 = SubTask.objects.get(title="Create slides")
# subtask_2.title = 'Create and format presentation slides'
# subtask_2.save()
#
#
# # Удалите задачу "Prepare presentation" и все ее подзадачи.
# Task.objects.filter(title="Prepare presentation").delete()