from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from backend import views

# Tristan: added more urls, removed auth/login and auth/logout
# these can be added later once/if we add our own views for logging in
# and loggin out. We should definitely reuse the rest_framework code for this
# however
urlpatterns = [
    url(r'^mysys/$', views.mysys),
    # url(r'^group/users/$', views.group_users),
    # url(r'^group/tag/$', views.group_tag),
    url(r'^filter/$', views.filter_systems),
    url(r'^filters/$', views.filters),
    # url(r'^systems/$', views.systems),
    url(r'^neena/thota/$', views.index),
]

# Tristan: just following django rest tutorial
# urlpatterns += format_suffix_patterns([
#     url(r'^systems/$', views.system_list),
#     url(r'^systems/(?P<pk>[0-9]+)$', views.system_detail),
#
#     url(r'^systems/$', views.SystemList.as_view()),
#     url(r'^systems/(?P<pk>[0-9]+)$', views.SystemDetail.as_view()),
#     url(r'^users/$', views.UserList.as_view()),
#	  url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
#	  url(r'^search/?SrchTerm=<str>&SrchType=<str>$', views.search),
# ])

# Tristan: Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'systems/test', views.SystemViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'group/systems', views.GroupSystemsViewSet)
router.register(r'group/tag', views.GroupTagViewSet)
# purely for deleting
router.register(r'group/tag/delete', views.GroupTagDeleteViewSet)
router.register(r'search', views.SearchViewSet)
router.register(r'fields', views.FieldsViewSet)
router.register(r'group/users', views.GroupUserViewSet)
router.register(r'systems', views.MySystemsViewSet)

# Tristan: The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns += [
    url(r'^', include(router.urls)),
]
