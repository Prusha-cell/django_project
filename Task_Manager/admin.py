from django.contrib import admin

from Task_Manager.models import Category, Task, SubTask


# Создание класса администратора для модели Category
class CategoryAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name',)
    # Задание полей, по которым будет производиться поиск
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 2


# Создание класса администратора для модели Task
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('short_title', 'description', 'status')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('title', 'status')
    # Определение порядка сортировки объектов в админке
    ordering = ('-title', 'status')
    # Определение количества объектов, отображаемых на одной странице в списке
    list_per_page = 10

    def short_title(self, obj):
        """В списке задач будет показана укороченная версия, если заголовок длинный."""
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title

    # Title будет отображаться при выборе задач
    short_title.short_description = 'Title'


admin.site.register(Task, TaskAdmin)


# Создание класса администратора для модели SubTask
class SubTaskAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('title', 'description', 'status')
    # Задание полей, по которым будет производиться поиск
    search_fields = ('title', 'created_at')
    # Добавление боковых фильтров для быстрого поиска по указанным полям
    list_filter = ('title', 'status')

    def to_status_done(self, request, queryset):
        queryset.update(status='done')

    to_status_done.short_description = 'Перевести статус в "done"'
    actions = [to_status_done]


admin.site.register(SubTask, SubTaskAdmin)
