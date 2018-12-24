from django.urls import path, include, re_path
from .views import ContactPage

urlpatterns = [
    path('', ContactPage, name="contact-page"),
]
