from django.contrib.auth.models import User

class EmailBackend(object):
	def authenticate(self, username=None, password=None, **kwargs):
		try : 
			user = User.objects.get(username__iexact=username)	
		except:
			return None

		if user.check_password(password):
			return user

		return None

	def get_user(self, user_id):
		try :
			return User.objects.get(pk=user_id)
		except:
			return None