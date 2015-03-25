from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from tastypie.utils import trailing_slash
from tastypie_actions.actions import actionurls, action
from django.conf.urls import url
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from child.models import Child, UserLogin
from child.smartAuthentication import SmartAuthentication
from tastypie.cache import SimpleCache
from django.db import IntegrityError
from tastypie.exceptions import BadRequest	
import logging

logger = logging.getLogger(__name__)


class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		allowed_methods = ['post']
		resource_name = 'auth'
		object_class = User
		include_resource_uri = False
		
		extra_actions = [
		{
			"name": "token",
			"http_method": "POST",
			"resource_type": "list",
			"summary": "Get Access Token",
			"fields": {
				"username": {
					"type": "string",
					"required": True,
					"description": "Username"
				},
				"password": {
					"type": "string",
					"required": True,
					"description": "Password"
				},
			}
		}]

	def prepend_urls(self):
		return actionurls(self)


	@action(name='token', allowed=['post'], static=True)
	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		logger.debug("inside login")
		print "login"
		try:
			if request.META.has_key('HTTP_AUTHORIZATION'):
				try:
					authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
					if authmeth.lower() == 'basic':
						auth = auth.strip().decode('base64')
						username, password = auth.split(':', 1)
						logger.debug("inside Http u: ".join(username))
				except Exception:
					return self.create_response(request, {
					'success': False,
					'reason': 'Invalid Header',
					}, HttpBadRequest )
			
			else:
				try:
					#data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
					if request.GET.get('username') and request.GET.get('password'):
						username = request.GET.get('username', '')
						password = request.GET.get('password', '')
					else:
						raise Exception("Invalid Content")
				except Exception:
					return self.create_response(request, {
					'success': False,
					'reason': 'Invalid Content or Missing Content',
					}, HttpBadRequest )

			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					request.user = user
					try:
						obj = UserLogin.objects.get(user=user)

						if obj:
							print "already login"
							expire_date = obj.expire_date
							access_token = obj.access_token
							refresh_token = obj.refresh_token

					except Exception, e:
						logger.info(str(e))
						expire_date = datetime.now() + timedelta(seconds=3600)
						access_token = user.password
						refresh_token = user.username
						access = UserLogin.objects.create(user=user, access_token=access_token, refresh_token=refresh_token, expire_date=expire_date)
						access.save()

					return self.create_response(request, {
						'success': True,
						'access_token': access_token,
						'refresh_token': refresh_token,
						'expire_date': expire_date
					})
				else:
					return self.create_response(request, {
						'success': False,
						'reason': 'disabled',
						}, HttpForbidden )
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'incorrect username or password',
					}, HttpUnauthorized )
		except Exception, e:
			logger.debug(str(e))

	@action(name='logout', allowed=['get'], static=True)
	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		print str(request.user)
		if request.user and request.user.is_authenticated():
			user=User.objects.get(username=request.user)
			print str(user)
			logout(request)
			obj = UserLogin.objects.get(user=user)
			obj.delete()
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)

class ChildResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Child.objects.all()
		resource_name = 'child'
		include_resource_uri = False
		allowed_methods = ['get', 'put', 'delete', 'post']
   		authorization= DjangoAuthorization()
		authentication = SmartAuthentication()
		cache = SimpleCache(cache_name='resources')
