" URL definitions "

from django.conf.urls.defaults import url, patterns

username = '(?P<username>[-\w]+)'

urlpatterns = patterns('jetpack.views',

    # browsing packages
    url(r'^addons/$', 'browser', {'type_id': 'a'},
        name='jp_browser_addons'),
    url(r'^libraries/$', 'browser', {'type_id': 'l'},
        name='jp_browser_libraries'),
    url(r'^addons/(?P<page_number>\d+)/$',
        'browser', {'type_id': 'a'}, name='jp_browser_addons_page'),
    url(r'^libraries/(?P<page_number>\d+)/$',
        'browser', {'type_id': 'l'}, name='jp_browser_libraries_page'),
    # by user
    url(r'^addons/by/%s/$' % username,
        'browser', {'type_id': 'a'}, name='jp_browser_user_addons'),
    url(r'^libraries/by/%s/$' % username,
        'browser', {'type_id': 'l'}, name='jp_browser_user_libraries'),
    url(r'^addons/by/%s/(?P<page_number>\d+)/$' % username,
        'browser', {'type_id': 'a'},
        name='jp_browser_user_addons_page'),
    url(r'^libraries/by/%s/(?P<page_number>\d+)/$' % username,
        'browser', {'type_id': 'l'},
        name='jp_browser_user_libraries_page'),

    url(r'^get_latest_revision_number/(?P<package_id>\d+)/$',
        'get_latest_revision_number', name='jp_get_latest_revision_number'),

    url(r'^addon/new/upload_xpi/$', 'upload_xpi', name='jp_upload_xpi'),

    # create new add-on/library
    url(r'^addon/new/',
        'create', {"type_id": "a"}, name='jp_addon_create'),
    url(r'^library/new/',
        'create', {"type_id": "l"}, name='jp_library_create'),


    # display details of the PackageRevision
    url(r'^addon/(?P<id_number>[-\w]+)/latest/$',
        'view_or_edit', {'type_id': 'a', 'latest': True},
        name='jp_addon_latest'),
    url(r'^library/(?P<id_number>[-\w]+)/latest/$',
        'view_or_edit', {'type_id': 'l', 'latest': True},
        name='jp_library_latest'),
    url(r'^addon/(?P<id_number>[-\w]+)/$',
        'view_or_edit', {'type_id': 'a'}, name='jp_addon_details'),
    url(r'^library/(?P<id_number>[-\w]+)/$',
        'view_or_edit', {'type_id': 'l'},  name='jp_library_details'),
    url(r'^addon/(?P<id_number>[-\w]+)/version/(?P<version_name>.*)/$',
        'view_or_edit', {'type_id': 'a'},
        name='jp_addon_version_details'),
    url(r'^library/(?P<id_number>[-\w]+)/version/(?P<version_name>.*)/$',
        'view_or_edit', {'type_id': 'l'},
        name='jp_library_version_details'),
    url(r'^addon/(?P<id_number>[-\w]+)/revision/(?P<revision_number>\d+)/$',
        'view_or_edit', {'type_id': 'a'},
        name='jp_addon_revision_details'),
    url(r'^library/(?P<id_number>[-\w]+)/revision/(?P<revision_number>\d+)/$',
        'view_or_edit', {'type_id': 'l'},
        name='jp_library_revision_details'),

    # get full module info
    url(r'^get_module/(?P<id_number>[-\w]+)/(?P<revision_number>\d+)/'
            '(?P<filename>.*)$', 'get_module', name='jp_get_module'),
    url(r'^module/(?P<pk>\d+)/$', 'download_module', name='jp_module'),

    # copy a PackageRevision
    url(r'^addon/copy/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'copy', {'type_id': 'a'}, name='jp_addon_revision_copy'),
    url(r'^library/copy/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'copy', {'type_id': 'l'},  name='jp_library_revision_copy'),

    # get Package revisions list
    url(r'^revisions_list/(?P<id_number>[-\w]+)$',
        'get_revisions_list_html', name='jp_revisions_list_html'),
    url(r'^revisions_list/(?P<id_number>[-\w]+)/(?P<revision_number>\d+)/$',
        'get_revisions_list_html', name='jp_revisions_list_html'),

    # save packagerevision
    url(r'^addon/save/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'save', {'type_id': 'a'}, name='jp_addon_revision_save'),
    url(r'^library/save/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'save', {'type_id': 'l'},  name='jp_library_revision_save'),

    # disable/activate/delete package
    url(r'^package/disable/(?P<id_number>[-\w]+)/$',
        'disable', name='jp_package_disable'),
    url(r'^package/activate/(?P<id_number>[-\w]+)/$',
        'activate', name='jp_package_activate'),
    url(r'^package/delete/(?P<id_number>[-\w]+)/$',
        'delete', name='jp_package_delete'),

    # get all, conflicting modules
    url(r'^revision/(?P<pk>\d+)/get_modules_list/$',
        'get_revision_modules_list', name='jp_revision_get_modules_list'),
    url(r'^revision/(?P<pk>\d+)/get_conflicting_modules_list/$',
        'get_revision_conflicting_modules_list',
        name='jp_revision_get_conflicting_modules_list'),

    # add/remove module
    url(r'^addon/add_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'add_module',
        {'type_id': 'a'}, name='jp_addon_revision_add_module'),
    url(r'^library/add_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'add_module',
        {'type_id': 'l'},  name='jp_library_revision_add_module'),
    url(r'^addon/remove_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_module',
        {'type_id': 'a'}, name='jp_addon_revision_remove_module'),
    url(r'^library/remove_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_module',
        {'type_id': 'l'},  name='jp_library_revision_remove_module'),

    # rename module
    url(r'^addon/rename_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'rename_module',
        {'type_id': 'a'}, name='jp_addon_revision_rename_module'),
    url(r'^library/rename_module/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'rename_module',
        {'type_id': 'l'}, name='jp_library_revision_rename_module'),

    # switch SDK version
    url(r'^addon/switch_sdk/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'switch_sdk', name='jp_addon_switch_sdk_version'),

    # add/remove attachment
    url(r'^addon/upload_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'upload_attachment',
        {'type_id': 'a'}, name='jp_addon_revision_upload_attachment'),
    url(r'^library/upload_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'upload_attachment',
        {'type_id': 'l'},  name='jp_library_revision_upload_attachment'),
    url(r'^revision/(?P<pk>\d+)/add_attachment/',
        'revision_add_attachment', name='jp_revision_add_attachment'),
    url(r'^addon/remove_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_attachment',
        {'type_id': 'a'}, name='jp_addon_revision_remove_attachment'),
    url(r'^library/remove_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_attachment',
        {'type_id': 'l'},  name='jp_library_revision_remove_attachment'),

     # rename attachment
    url(r'^addon/rename_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'rename_attachment',
        {'type_id': 'a'}, name='jp_addon_revision_rename_attachment'),
    url(r'^library/rename_attachment/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'rename_attachment',
        {'type_id': 'l'}, name='jp_library_revision_rename_attachment'),

    #add empty dir
    url(r'^addon/add_folder/(?P<id_number>[-\w]+)/revision'
            '(?P<revision_number>\d+)/$',
        'add_folder',
        {'type_id': 'a'}, name='jp_addon_revision_add_folder',
        ),
    url(r'^library/add_folder/(?P<id_number>[-\w]+)/revision'
            '(?P<revision_number>\d+)/$',
        'add_folder',
        {'type_id': 'l'}, name='jp_library_revision_add_folder',
        ),

    #remove empty dir
    url(r'^addon/remove_folder/(?P<id_number>[-\w]+)/revision'
            '(?P<revision_number>\d+)/$',
        'remove_folder',
        {'type_id': 'a'}, name='jp_addon_revision_remove_folder',
        ),
    url(r'^library/remove_folder/(?P<id_number>[-\w]+)/revision'
            '(?P<revision_number>\d+)/$',
        'remove_folder',
        {'type_id': 'l'}, name='jp_library_revision_remove_folder',
        ),

    # display attachment
    url(r'^attachment/(?P<uid>.*)$',
        'download_attachment', name='jp_attachment'),

    # autocomplete library
    url(r'^autocomplete/library/$',
        'library_autocomplete', name='jp_library_autocomplete'),
    # assign library
    url(r'^addon/assign_library/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'assign_library',
        {'type_id': 'a'}, name='jp_addon_revision_assign_library'),
    url(r'^library/assign_library/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'assign_library',
        {'type_id': 'l'}, name='jp_library_revision_assign_library'),

    # update library
    url(r'^addon/update_library/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'update_library',
        {'type_id': 'a'}, name='jp_addon_revision_update_library'),
    url(r'^library/update_library/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'update_library',
        {'type_id': 'l'}, name='jp_library_revision_update_library'),

    # remove library
    url(r'^addon/remove_dependency/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_library',
        {'type_id': 'a'}, name='jp_addon_revision_remove_library'),
    url(r'^library/remove_dependency/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'remove_library',
        {'type_id': 'l'},  name='jp_library_revision_remove_library'),

    # check libraries for latest versions
    url(r'addon/check_latest_dependencies/(?P<id_number>[-\w]+)/revision/'
            '(?P<revision_number>\d+)/$',
        'latest_dependencies',
        {'type_id': 'a'}, name='jp_addon_check_latest_dependencies'),

    url(r'library/check_latest_dependencies/(?P<id_number>[-\w]+)/revision'
            '(?P<revision_number>\d+)/$',
        'latest_dependencies',
        {'type_id': 'l'}, name='jp_library_check_latest_dependencies'),
)
