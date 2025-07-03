from django.shortcuts import render
from django.http import HttpResponse
from project.models import Project
from django.utils import timezone

def test(req):
    # new_project = Project(name='new_project', lang='py', description='test')
    # new_project.save()  # создание экземпляра модели и сохранение его в базу

    # del_obj = Project.objects.filter(id__gt=5)
    # del_obj.delete()    # удаление экземпляра через фильтр

    # Project.objects.create(name='old_project', lang='C#', description='test_2')  # создание экземпляра без прописывания save()
    return HttpResponse('Мы пришли с миром!!!')
