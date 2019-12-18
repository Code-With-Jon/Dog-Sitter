from django.shortcuts import render
# Add UdpateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# Add the following import
from django.http import HttpResponse
from .models import Dog, Toy, Photo
# Import the FeedingForm
from .forms import FeedingForm
from django.shortcuts import render, redirect
import uuid
import boto3



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
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
    return render(request, 'dogs/detail.html', {
        # include the dog and feeding_form in the context
        'dog': dog, 'feeding_form': feeding_form, 'toys': toys_dog_doesnt_have
    })

# add this new function below dogs_detail


def add_feeding(request, dog_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the dog_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

def assoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)

def unassoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)

class DogCreate(CreateView):
    model = Dog
    fields = '__all__'


class DogUpdate(UpdateView):
    model = Dog
    fields = ['breed', 'description', 'age']


class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def add_photo(request, dog_id):
  S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
  BUCKET = 'dog-sitter'
    # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          # build the full url string
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          # we can assign to cat_id or cat (if you have a cat object)
          photo = Photo(url=url, dog_id=dog_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', dog_id=dog_id)