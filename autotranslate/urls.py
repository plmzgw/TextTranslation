from django.conf.urls import patterns, include, url

urlpatterns = patterns('autotranslate.views',
    url(r'^$', 'upload_file', name = 'filelist'),
    url(r'^test/$', 'test', name='test'),
    url(r'^file/(\w+)/del_up/$', 'delete_upfile', name='delete_upfile'),
    url(r'^file/(\w+)/del_trans/$', 'delete_transfile', name='delete_transfile'),
    url(r'^file/(\w+)/resolve/$', 'resolve_file', name='resolve_file'),
    url(r'^file/translate/$', 'translate_file', name='translate'),
    url(r'^file/(\w+)/download/$', 'down_file', name='download'),

)
