from django.contrib import admin
from .models import Options, Titles, Emails, Voted
# Register your models here.

admin.site.register([Options, Titles, Emails, Voted] )