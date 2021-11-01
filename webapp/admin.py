from ast import Sub
from django.contrib import admin

from .models import User, City, Submission, Comparison


# Register your models here.
admin.site.register(City)
admin.site.register(Submission)
admin.site.register(Comparison)
