from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from main.views import main_views, profile_views, authorization_views, servers, control_panel_views, api, api_payment
from project import settings

urlpatterns = [
    path('', main_views.index_page, name="home"),
    path('admin/', admin.site.urls, name="Админ. панель"),
    path('servers/', servers.servers_page, name="servers"),
    path('create_server/', servers.create_server_page, name="create server"),
    # profile
    path('profile/', profile_views.profile_page, name="profile"),
    path('profile/edit_username/', profile_views.change_username, name="edit username"),
    path('profile/edit_password/', profile_views.change_password, name="edit password"),
    path('profile/edit_email/', profile_views.change_email, name="edit email"),
    path('profile/edit_logo/', profile_views.change_logo, name="edit logo"),
    # auth
    path('registration/', authorization_views.RegisterUser.as_view(), name="register"),
    path('login/', authorization_views.LoginUser.as_view(), name="login"),
    path('logout/', authorization_views.logout_user, name='logout'),
    # control_panel
    path('server/<int:server_id>/console', control_panel_views.console_page, name='console'),
    path('server/<int:server_id>/settings', control_panel_views.settings_page, name='settings'),
    path('server/<int:server_id>/world', control_panel_views.world_page, name='world'),
    path('server/<int:server_id>/payment', control_panel_views.payment_page, name='payment'),
    path('server/<int:server_id>/delete', control_panel_views.delete_page, name='delete'),
    # api
    path('api/create_server', api.create_server),
    path('api/start_server/<int:server_id>', api.start_server),
    path('api/stop_server/<int:server_id>', api.stop_server),
    path('api/restart_server/<int:server_id>', api.restart_server),
    path('api/edit_server/<int:server_id>', api.edit_server),
    path('api/run_command/<int:server_id>', api.run_command),
    path('api/edit_version/<int:server_id>', api.edit_version_server),
    path('api/delete_world/<int:server_id>', api.delete_world),
    path('api/set_modpack/<int:server_id>', api.set_modpack),
    path('api/delete_server/<int:server_id>', api.delete_server),
    # payment
    path('api/payment/yoomoney', api_payment.yoomoney),
    path('api/payment/create_payment', api_payment.create_payment, name='create payment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.main_views.page_not_found_view'