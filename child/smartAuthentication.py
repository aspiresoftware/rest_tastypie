from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest
from datetime import datetime, timedelta
from tastypie.authentication import Authentication
from models import UserLogin
import logging

"""
This is the custom authentication implementation using Authentication

"""


class OAuthError(RuntimeError):
	"""Generic exception class."""
	def __init__(self, message="Authentication faield"):
		self.message = message


class SmartAuthentication(Authentication):
	def __init__(self, realm='API'):
		self.realm = realm

	def is_authenticated(self, request, **kwargs):
		"""
		Verify authentication. Parameters accepted as
		values in "Authorization" header, or as a GET request
		or in a POST body.
		"""

		try:
			auth_header_value = request.META.get('HTTP_AUTHORIZATION', '')

			if auth_header_value:
				authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
			else:
				auth = request.GET.get('api_key')
				authmeth = "bearer"
			if not auth:
				logging.error('SmartAuthentication. No access_token found.')
				return None

			if not authmeth.lower() == 'bearer':
				logging.error('SmartAuthentication. No authentication method is invalid.')
				return None

			"""
			If verify_access_token() does not pass, it will raise an error
			"""

			token = SmartAuthentication.verify_access_token(auth)

			return True
		except KeyError, e:
			logging.exception("Error in Authentication.")
			request.user = AnonymousUser()
			return False
		except Exception, e:
			logging.exception("Error in Authentication.")
			return False

		return True
	
	@staticmethod
	def verify_access_token(auth):
		# Check if key is in AccessToken key
		try:
			token = UserLogin.objects.get(access_token=auth)

			# Check if token has expired
			if token.expire_date < timezone.now():
				token.delete()
				raise Exception("AccessToken has expired.")
		except UserLogin.DoesNotExist, e:
			raise OAuthError("AccessToken not found at all.")
		token.expire_date = datetime.now() + timedelta(seconds=3600)
		token.save()
		logging.debug('Valid access')
		return token