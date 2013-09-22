from django.views.generic import RedirectView
from django.conf.urls.defaults import patterns, include, url
from booliwood.main.views import show, update

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^update$', update),
    url(r'^$', show),
    url(r'', RedirectView.as_view(url='/')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
