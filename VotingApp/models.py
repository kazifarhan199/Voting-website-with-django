from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Emails(models.Model):
	email = models.CharField(max_length=40)

	def __str__(self):
		return self.email

class Voted(models.Model):
	title = models.ForeignKey('Titles',on_delete=models.CASCADE)
	email = models.ForeignKey('Emails',on_delete=models.CASCADE)		

class Titles(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	end = models.DateTimeField(auto_now_add=False, )
	published = models.CharField(max_length=1, default='0')
	emailed = models.CharField(max_length=1, default='0')
	
	def __str__(self):
		return self.title

class Options(models.Model):
	image = models.ImageField(blank=True)
	url = models.URLField(default="https://amzn.to/2vRFY1m")

	button_url = models.URLField(default='''
			http://g-ec2.images-amazon.com/images/G/31/img14/anywhere/amazon-logo-500500._V327001990_.jpg
		''')
	
	detail1 = models.CharField(blank=True, max_length=300,default="")
	detail2 = models.CharField(blank=True, max_length=300,default="")
	detail3 = models.CharField(blank=True, max_length=300,default="")


	vote = models.IntegerField(default=0)
	cost = models.CharField(blank=True, max_length=1000000000000)
	name = models.CharField(max_length=300)
	title = models.ForeignKey('Titles',on_delete=models.CASCADE)

	def __str__(self):
		return self.name