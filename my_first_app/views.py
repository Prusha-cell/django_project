from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def hello(request):
    name = request.GET.get('name', 'Vadym')
    return HttpResponse(f"Hello {name}!")
