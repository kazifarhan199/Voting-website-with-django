from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.Login, name="login"),
    #If changing this alseo change LOGIN_URL in settings
    path('logout/', views.Logout, name="logout"),
    path('register/', views.Register, name='register'),
    path('change-password/', views.ChangePassword, name='change-password'),

	path(
		'password_reset/', 
		auth_views.password_reset,
		{
			'template_name':'AccountsApp/reset_password.html', 
			'email_template_name': 'AccountsApp/password_reset_email_template.html', 
			#Removed "{% trans "Your username, in case you've forgotten:" %} {{ user.get_username }}"
			# from default template template
			'subject_template_name':'AccountsApp/password_reset_email_subject.txt',
			#This is same as the default one
		}, 
		name='password_reset',
	),
	path(
		'password_reset/done/', 
		auth_views.password_reset_done,
		{
			'template_name':'AccountsApp/reset_password_reset.html'
		} ,
		name='password_reset_done'
	),
	path(
		'reset/<uidb64>/<token>/',
		auth_views.password_reset_confirm,
		{
			'template_name':'AccountsApp/reset_password_confirm.html'
		}, 
		name='password_reset_confirm'
	),
	path(
		'reset/done/', 
		auth_views.password_reset_complete,
		{
			'template_name':'AccountsApp/password_reset_complete.html'
		}, 
		name='password_reset_complete'
	),
]