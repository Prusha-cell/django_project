from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer
from .models import Task
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse


# создание новой задачи
@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# вывод всех задач
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# получение одной конкретной задачи
@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


# # Вычисление общего количества задач
# def get_count_tasks(requests):
#     aggregates = Task.objects.aggregate(total_tasks=Count('id'))
#     print(f"Общее количество задач: {aggregates['total_tasks']}")


# статистика задач
def display_statistic_tasks(requests):
    now = timezone.now()

    total_tasks = Task.objects.count()
    status_counts = Task.objects.values('status').annotate(count=Count('id'))
    overdue_tasks = Task.objects.filter(deadline__lt=now).exclude(status='done').count()

    return JsonResponse({
        "total_tasks": total_tasks,
        "status_counts": {item['status']: item['count'] for item in status_counts},
        "overdue_tasks": overdue_tasks
    }, status=status.HTTP_200_OK)