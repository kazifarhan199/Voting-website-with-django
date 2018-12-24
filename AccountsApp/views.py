from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_reset
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from VotingApp.models import Emails
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def Register(request):
	data = {"title":"Register", }
	if request.user.is_authenticated:
		return redirect(reverse("pols", args=[4]))
	else:
		if request.method == "POST":
			if User.objects.filter(username__iexact=request.POST['username']).exists():
				data.update({'error':'Email already registered'})
				return render(request, 'AccountsApp/register.html',data)

			form = UserCreationForm(request.POST)
			if form.is_valid():
				data.update({'message':'User Created'})
				form.save()
				user = User.objects.get(username = request.POST['username'])
				user.email = request.POST['username']
				user.save()
				user_email = request.POST['username'].lower()
				if not(Emails.objects.filter(email=user_email).exists()):
					save_email = Emails.objects.create(email = user_email)
					save_email.save()
				return redirect(reverse("login"))
			else :
				data.update({'error':'Registeration Failed'})
				return render(request, 'AccountsApp/register.html',data)

		else:
			return render(request, 'AccountsApp/register.html',data)

def Login(request):
	data = {"title":"Login"}
	return login(request,
		template_name = "AccountsApp/login.html",
		authentication_form=LoginForm,
		redirect_authenticated_user=True,
		extra_context=data
	)	


@login_required
def Logout(request):		
	data = {'title':'Logout'}
	logout(request)
	return redirect(reverse('login'))

@login_required
def ChangePassword(request):
	data = {'title':'Change Password'}
	form = PasswordChangeForm(user=request.user)
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		form = PasswordChangeForm(data=request.POST, user=user)

		if form.is_valid():
			form.save()
			messages.success(request, "you'r new password has been saved")
			#As user has loged out we are using form.user to refer user
			update_session_auth_hash(request, form.user)
			return redirect(reverse('dashboard'))
		else:
			data.update({'error':'Password change Failed'})

	data.update({'form':form})
	return render(request, 'AccountsApp/change_password.html', data)

