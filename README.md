# rest_tastypie

REST based tastypie project structure

Project structure using tastypie, swagger, mqsql :

prerequisite : python2.7+,tastypie, mqsql

Steps :

(1) git clone https://github.com/aspiresoftware/rest_tastypie

(2) cd rest_tastypie/

(3) create database as per the rest_tastypie/settings.py
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql', 
	        'NAME': 'rest_tastypie',
	        'USER': 'root',
	        'PASSWORD': 'root',
	        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
	        'PORT': '3306',
	    }
	}

(4) python manage.py migrate

(5) python manage.py runserver

(6) Enjoy the app from browser : http://127.0.0.1:8000/api/doc/
