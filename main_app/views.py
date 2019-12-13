from django.shortcuts import render

# Add the following import
from django.http import HttpResponse
from django.shortcuts import render


# Define the home view
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def dogs_index(request):
    return render(request, 'dogs/index.html', {'dogs': Dogs})

# Add the Cat class & list and view function below the imports


class Dog:  # Note that parens are optional if not inheriting from another class
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age


Dogs = [
    Dog('Cody', 'Mixed', 'Very Playful!', 3),
    Dog('Buddy', 'Golden-Doodle', 'Cuddle Bug', 0),
    Dog('Raven', 'Shiba Inu', '3 legged trouble maker', 4)
]
