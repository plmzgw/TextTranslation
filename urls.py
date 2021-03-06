from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TextTranslate.views.home', name='home'),
    url(r'^', include('autotranslate.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)

urlpatterns+=patterns('',
                      (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT+settings.STATIC_URL}),
                      )


