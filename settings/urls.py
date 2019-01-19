from django.conf.urls import include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from backend import views

# Tristan: Added rest_framework auth/urls, we might also want to change the auth/login to
# use our own views, but reusing code from the rest_framework. Also react app can be added
# as a view later
urlpatterns = [
    url(r'^$',views.ReactAppView.as_view()),
    url(r'^admin/', admin.site.urls),

    url(r'^', include('backend.urls')),
    url(r'^auth/', include('rest_framework.urls')),
]