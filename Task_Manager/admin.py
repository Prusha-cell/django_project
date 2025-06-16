from django.contrib import admin

from Task_Manager.models import Category, Task, SubTask


# Создание класса администратора для модели Category
class CategoryAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name',)
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


# Создание класса администратора для модели Task
class TaskAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('title', 'description', 'status')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('title', 'status')
    # Определение порядка сортировки объектов в админке
    ordering = ('-title', 'status')
    # Определение количества объектов, отображаемых на одной странице в списке
    list_per_page = 10


admin.site.register(Task, TaskAdmin)


# Создание класса администратора для модели SubTask
class SubTaskAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('title', 'description', 'status')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('title', 'created_at')
    # Добавление боковых фильтров для быстрого поиска по указанным полям
    list_filter = ('title', 'status')


admin.site.register(SubTask, SubTaskAdmin)
