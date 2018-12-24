from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse

def ContactPage(request):
	form = ContactForm()
	data = {'form':form,'title':'Contact us'}
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request,'ContactApp/done.html', data)
		else:
			print(form)
			error = "The action failed "
			data.update({'error':error})


	return render(request,'ContactApp/contact.html',data)
