from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url('^builder.webapp$', 'base.views.app_manifest'),
    url('^robots.txt$', 'base.views.robots'),
    url('^services/graphite/(prod|stage|trunk)$', 'base.views.graphite',
        name='graphite'),
    url('^services/monitor$', 'base.views.monitor', name='monitor'),
    url('^services/settings$', 'base.views.site_settings', name='settings'),
    url('^services/admin$', 'base.views.admin', name='admin_triggers'),
)
