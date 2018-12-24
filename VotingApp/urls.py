from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('polls/<id>/', views.VoteView, name="pols"),
    path('dashboard/', views.PanelView, name='dashboard'),
    #If changing this alseo change LOGIN_REDIRECT_URL in settings
    path('dashboard/titles/<id>/', views.TitlesView, name='titles'),
    path('dashboard/delete/<id>/', views.DeleteTitle, name='delete'),
    path('dashboard/edit/<id>/', views.EditOption, name='edit'),
    path('dashboard/option/delete/<id>/', views.DeleteOption, name='deleteOption'),
    path('dashboard/titles/edit/<id>/', views.TitleEdit, name='titleEdit'),
]