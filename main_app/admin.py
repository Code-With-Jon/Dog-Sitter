from django.contrib import admin

# Register your models here.
from .models import Dog, Feeding, Toy

# Register your models here
admin.site.register(Dog)

# register the new Feeding Model
admin.site.register(Feeding)

# register the new Toy Model
admin.site.register(Toy)