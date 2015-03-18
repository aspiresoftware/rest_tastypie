from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from child.models import Child
from tastypie.cache import SimpleCache
	

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        #fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        include_resource_uri = False
        resource_name = 'user'
        cache = SimpleCache()
   
class ChildResource(ModelResource):
	#user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Child.objects.all()
		resource_name = 'child'
		allowed_methods = ['get', 'post', 'put', 'delete']
   		fields = ['first_name','last_name','email']
		authorization= DjangoAuthorization()
		authentication = BasicAuthentication()
		cache = SimpleCache(cache_name='resources')
