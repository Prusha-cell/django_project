from django.db import models

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

