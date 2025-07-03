from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

LANG_CHOICES = {
    'py': 'Python',
    'java': 'Java',
    'c#': 'C#'
}

TAG_CHOICES = {
    'backend': 'Backend',
    'frontend': 'Frontend',
    'q&a': 'Q&A',
    'design': 'Design',
    'devOPS': 'DevOPS'
}

GRADE_CHOICES = {
    'junior': 'Junior',
    'middle': 'Middle',
    'senior': 'Senior',
}

STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'done': 'Done',
    'closed': 'Closed',
    'blocked': 'Blocked',
    'pending': 'Pending'
}

PRIORITY_CHOICES = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'very_high': 'Very High'
}





class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(choices=LANG_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)  #

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, choices=TAG_CHOICES)
    projects = models.ManyToManyField('Project', related_name='tags', blank=True)  #связь между моделями

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=255)
    grade = models.CharField(choices=GRADE_CHOICES)
    projects = models.ManyToManyField('Project', related_name='developers', blank=True)


class Task(models.Model):
    name = models.CharField(unique=True, validators=[MinLengthValidator(10)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)