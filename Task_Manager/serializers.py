from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


# вывод всех задач
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']


# создание новой задачи
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past")
        return value


# список всех задач
class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['owner']


# вывод одной конкретной задачи с подзадачами
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # Вложенный сериализатор

    class Meta:
        model = Task
        fields = '__all__'  # Включает все поля модели


# создание одной подзадачи
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'


# Вывод всех категорий
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# создание и обновление категории
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Please, provide a valid category name.")

        return value

    def create(self, validated_data):
        category_name = validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError(
                {"name": "Категория с таким названием уже существует."}
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        category_name = validated_data.get('name')
        if category_name and Category.objects.exclude(pk=instance.pk).filter(name=category_name).exists():
            raise serializers.ValidationError(
                {"name": "Категория с таким названием уже существует."}
            )
        return super().update(instance, validated_data)
