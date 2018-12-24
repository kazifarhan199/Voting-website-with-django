from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.utils.translation import  gettext_lazy
from VotingApp.views import tester

#Changing some values on admin page
admin.site.site_title = gettext_lazy("Let's Vote")
admin.site.site_header = gettext_lazy("Let's Vote")
admin.site.index_title = gettext_lazy("Let's Vote")

#to use other template for admin
# admin.site.index_template = 'index.html'
# admin.autodiscover()

#To Customise error 404, 500, 403, 400 
#look https://docs.djangoproject.com/en/2.1/topics/http/views/#customizing-error-views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('test/<id>/', tester, name='0'),

    path('',include('VotingApp.urls')),
    path('account/',include('AccountsApp.urls')),
    path('contact/',include('ContactApp.urls')),

    re_path(r'media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]