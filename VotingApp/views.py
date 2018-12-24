import datetime
from django.utils.timezone import utc
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import OptionForm, TitleForm
from .models import Emails, Options, Titles, Voted
from django.contrib import messages
import time
from django.core.mail import send_mail
from django.conf import settings

# def SendResults(title):
# 	if title.emailed == '0' and title.published == '1':
# 		title.emailed = 1
# 		title.save()
# 		voted = Voted.objects.filter(title = title)
# 		if len(voted) != 0:
# 			for email in voted:
# 				send_mail(
# 			    'Results for '+str(title),
# 			    'The results for '+str(title)+'\nHave been declared at :'+str(settings.MY_SITE_NAME)+'\nCheck it out \nHear '+str(settings.MY_SITE_NAME)+str(reverse('pols', args=[title.id])),
# 			    from_email = settings.EMAIL_HOST_USER,
# 			    recipient_list=[email.email],
# 			    fail_silently=False,
# 			)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
	titles = Titles.objects.filter(published ='1').order_by('-id')
	data = {'title':'Home', 'titles':titles}
	return render(request, 'VotingApp/home.html', data)

def TitleEdit(request,id):
	if request.method == "POST":
		title = get_object_or_404(Titles, id=id)
		if title.published == '0':
			d=1
			title.title = request.POST['title']
			try:
				days = int(request.POST['end_in'])
				title.published =1
				date = utc.localize(datetime.datetime.today()) + datetime.timedelta(days=days)
				title.end = date
				title.save()

			except:
				title.save()

	return redirect(reverse('titles',args=[id]))

def VoteView(request, id):
	data = {}
	d=0
	title = get_object_or_404(Titles, id=id)
	now = utc.localize(datetime.datetime.utcnow())	

	options = Options.objects.filter(title=title)
	data = {"options": options, "title": title}

	if title.published == '0':
		data.update({'error':'Preview Mode'})

		if title.user == request.user:
			data.update({'this':'true'})
		return render(request, 'VotingApp/index.html', data)

	title.end = title.end+datetime.timedelta(hours=6) - datetime.timedelta(minutes=30)

	if title.end <= now:
		# SendResults(title)
		data.update({'error':'Polls have ended results are'})
		return render(request, 'VotingApp/index.html', data)
	# now = now.replace(tzinfo=utc).strftime('%D: %H:%M:%S')
	
	time_left = (title.end-now-datetime.timedelta(hours=5)-datetime.timedelta(minutes=30))	
	data.update({"time_left" : str(time_left)[:-7]})

	if request.method == "POST" and d == 0:
		user_email = get_client_ip(request)
		if Emails.objects.filter(email=user_email).exists():
			newemail = Emails.objects.filter(email=user_email)[0]
		else:
			newemail = Emails.objects.create()
			newemail.email = user_email
			newemail.save()

		emailss =  Voted.objects.filter(email=newemail)

		if emailss.filter(title=title).exists():
			data.update({'error' : "You have already placed a vote !!"})
			return render(request, 'VotingApp/index.html', data)

		instance = Options.objects.get(name=request.POST['name'])
		instance.vote +=1
		instance.save()

		Voted.objects.create(email=newemail, title=title)
		
		data.update({'message' : "Suckessfully Voted for "+ request.POST['name']})

	return render(request, 'VotingApp/index.html', data)


@login_required
def PanelView(request):
	r_message = messages.get_messages(request)
	data = {"title":"DashBoard", 'r_message':r_message}

	if request.method == "POST":
		name = request.POST['name']
		# days = request.POST['end_in']
		# days = int(days)
		time = datetime.datetime.today() + datetime.timedelta(days=1000)
		Titles.objects.create(user=request.user, title=name, end=time)

	titles = Titles.objects.filter(user=request.user)
	titles = titles.order_by('-id')
	data.update({'titles':titles})
	return render(request, 'VotingApp/panel.html', data)

@login_required
def TitlesView(request, id):
	r_message = messages.get_messages(request)
	title = get_object_or_404(Titles, id=id)
	data = {'title':title}
	if title.user == request.user:
		options = Options.objects.filter(title=title).order_by('-id')
		data.update({'object':title, 'options':options})
		if title.published == '0':
			if request.method == "POST":
				form = OptionForm(request.POST, request.FILES)
				form.title = title
				if form.is_valid():
					form.save()
				else:
					print(form)
					print("not saved")
				# print(str(request.PUT))
			# if request.method == "POST":
				# pass
				# print(str(request.POST))
		else:
			data.update({"time_left" : str(title.end)[:-7]})
		return render(request, 'VotingApp/title_detail.html', data)
	else:
		return redirect(reverse('pols', args=[id]))

@login_required
def DeleteTitle(request, id):
	title = get_object_or_404(Titles, id=id)
	if title.user == request.user:
		title.delete()

	return redirect('dashboard')

def tester(request, id):
	form = OptionForm()
	return render(request,'tester/t.html', {'form':form})

@login_required
def EditOption(request, id):
	option = get_object_or_404(Options, id=id)
	if option.title.user == request.user:
		if option.title.published == '0':
			print(option.id)
			if request.method == "POST":
				form = OptionForm(request.POST, request.FILES, instance=option)
				form.title = option.title
				
				if form.is_valid():
					form.save()					

				else:
					print('!!!!!!!!!!!!!!!!')
					print(form)
					print('!!!!!!!!!!!!!!!!')
					messages.success(request, "Change Failed")

	return redirect(reverse('titles', args=[option.title.id]))

@login_required
def DeleteOption(request, id):
	option = get_object_or_404(Options, id=id)
	if option.title.user == request.user:
		option.delete()

	return redirect(reverse('titles', args=[option.title.id]))
