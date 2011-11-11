from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('multi_editor.views',
    # Example:
    (r'^(?P<namespace>\w+)/(?P<name>\w+)/$', 'display'),
    (r'^save/$', 'save'),
    (r'^compile/$', 'compile'),
)
