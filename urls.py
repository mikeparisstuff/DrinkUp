from django.conf.urls import patterns, include, url
from django.contrib import admin

from users import views as users_views
from bars import views as bars_views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^rest-api/', include('rest_framework_swagger.urls')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),

    # Auth endpoints
    url(r'^auth/login/bytoken/$', users_views.LoginWithToken.as_view(), name='login_by_token'),
    url(r'^auth/login/byemail/$', users_views.LoginWithEmail.as_view(), name='login_by_email'),
    url(r'^auth/login/newuser/$', users_views.LoginNewUser.as_view(), name='login_new_user'),
    url(r'^auth/login/newbar/$', bars_views.LoginNewBarAdmin.as_view(), name='login_new_bar'),
    url(r'^auth/logout/$', users_views.Logout.as_view(), name='logout'),

    # Users API endpoints
    url(r'^users/users/$', users_views.ProfileList.as_view(), name='list_all_profiles'),
    url(r'^users/myprofile/$', users_views.MyProfile.as_view(), name='my_profile'),

    # Bar API endpoints
    url(r'^bars/bars/$', bars_views.BarList.as_view(), name='list_all_bars'),
    url(r'^bars/mybar/$', bars_views.MyBar.as_view(), name='my_bar'),
    url(r'^bars/mybar/initiate/$', bars_views.SetInitialInformation.as_view(), name='initiate_bar_information'),
    url(r'^bars/mybar/mymenu/$', bars_views.MyMenu.as_view(), name='my_bar\'s_menu'),
    url(r'^bars/bar/(?P<pk>[0-9]+)/$', bars_views.BarProfile.as_view(), name='display_bar_profile'),

)
