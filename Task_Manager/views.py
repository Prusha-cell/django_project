from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import (TaskCreateSerializer,
                          TaskListSerializer,
                          TaskDetailSerializer,
                          SubTaskSerializer)
from .models import Task, SubTask
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


# создание новой задачи
@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#вывод всех задач, а так же по дням недели
@api_view(['GET'])
def task_list(request):
    weekday_param = request.query_params.get('weekday', None)

    if weekday_param:
        # Преобразуем входной день недели в нижний регистр
        weekday_param = weekday_param.lower()

        # Словарь соответствий: день недели -> номер (0 - понедельник, 6 - воскресенье)
        weekdays_map = {
            'понедельник': 0,
            'вторник': 1,
            'среда': 2,
            'четверг': 3,
            'пятница': 4,
            'суббота': 5,
            'воскресенье': 6
        }

        if weekday_param not in weekdays_map:
            return Response({'error': 'Некорректный день недели. Используйте: понедельник, вторник, ...'},
                            status=status.HTTP_400_BAD_REQUEST)

        weekday_number = weekdays_map[weekday_param]
        tasks = Task.objects.all()

        # Фильтруем по дню недели из поля deadline
        tasks = [task for task in tasks if task.deadline.weekday() == weekday_number]
    else:
        # Если параметр не передан — показать все задачи
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


class SubTaskListCreateView(APIView):
    class CustomPagination(PageNumberPagination):
        page_size = 5
        page_size_query_param = 'page_size'
        max_page_size = 20

    def get_queryset(self, request):
        queryset = SubTask.objects.all().order_by('-created_at')

        # Получаем фильтры из параметров запроса
        task_title = request.query_params.get('task_title')
        status_param = request.query_params.get('status')

        if task_title:
            # Фильтрация по названию задачи через связь task__title
            queryset = queryset.filter(task__title__icontains=task_title)

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset(request)
        paginator = self.CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk: int) -> SubTask:
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        sub_task = self.get_object(pk=pk)

        serializer = SubTaskSerializer(sub_task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        sub_task = self.get_object(pk=pk)
        serializer = SubTaskSerializer(sub_task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        sub_task = self.get_object(pk=pk)
        sub_task.delete()
        return Response(
            data={"message": "Subtask was deleted successfully"},
            status=status.HTTP_200_OK
        )
