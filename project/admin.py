from django.contrib import admin

from project.models import Tag, Project, Developer, Task


# Создание класса администратора для модели Category
class TagAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name',)
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name',)


# Создание класса администратора для модели Category
class ProjectAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'description', 'lang', 'created_at')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name', 'description', 'lang')


# Создание класса администратора для модели Category
class DeveloperAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'grade')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name', 'grade')


# Создание класса администратора для модели Category
class TaskAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'project__name', 'description', 'status', 'priority', 'created_at', 'updated_at', 'due_date')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name', 'description', 'status', 'priority', 'created_at', 'updated_at')


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Task, TaskAdmin)
