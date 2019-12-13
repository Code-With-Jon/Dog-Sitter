from django.shortcuts import render

# Add the following import
from django.http import HttpResponse
from django.shortcuts import render
from .models import Dog


# Define the home view
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def dogs_index(request):
    dog = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dog': dog})


def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})
