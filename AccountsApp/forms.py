from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
	error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that the password "
            "fields is case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }