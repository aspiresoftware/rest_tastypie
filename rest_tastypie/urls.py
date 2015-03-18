from django.conf.urls import patterns, include, url
from tastypie.api import Api
from django.contrib import admin
from child.api.resources import ChildResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(ChildResource())
v1_api.register(UserResource())


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url(r'^api/', include(v1_api.urls)),
)
