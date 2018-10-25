import os
import sys
from django.conf import settings

settings.configure(
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	DEBUG=True,
	SECRET_KEY='thisisthesecretkey',
	ROOT_URLCONF=__name__,
	INSTALLED_APPS = [
	    'django.contrib.sessions',
		'django.contrib.messages',
    	'django.contrib.staticfiles',
	],
	MIDDLEWARE =[
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
	],
	TEMPLATES=[
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': ['templates']
		}
	],
	STATIC_URL = 'static/',
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend',
)

from django import forms

class ContactForm(forms.Form):
	contact_name = forms.CharField()
	contact_email = forms.EmailField()
	content = forms.CharField(
		required = True,
		widget=forms.Textarea
	)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['contact_name'].label = "your name"
		self.fields['contact_email'].label = "Your email"
		self.fields['content'].label = "Say something"

from django.template.loader import get_template
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import Context
from django.shortcuts import render,redirect

# The view goes here.
def index(request):
	form_class  = ContactForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = form.cleaned_data['contact_name']
			contact_email = form.cleaned_data['contact_email']
			form_content = form.cleaned_data['content']

			# email profile with content
			template = get_template('contact_template.txt')

			context = {
				'contact_name': contact_name,
				'contact_email': contact_email,
				'form_content': form_content,
			}
			content = template.render(context)
			email = EmailMessage(
				'New contact form submission',
				content,
				'Your website <hi@weddinglovely.com>',
				['patrickblaze2@gmail.com'],
				headers = {'Reply-To': contact_email }
			)
			email.send()
			messages.add_message(request, messages.SUCCESS, 'E-mail sent')
			return redirect('/')

	return render(request, 'contact.html', {
		'form': form_class,
	})

from django.conf.urls import url

urlpatterns = [
	url(r'^$', index),
]

if __name__ == "__main__" :
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)