from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from auction import views

urlpatterns = [
    path('admin/bid-view/', views.admin_bid_view, name='admin_bid_view'),
    path('admin/player-bids/<int:player_id>/', views.player_bid_detail, name='player_bid_detail'),
    path('admin/bid/<int:bid_id>/approve/', views.approve_bid_action, name='approve_bid'),
    path('admin/bid/<int:bid_id>/reject/', views.reject_bid_action, name='reject_bid'),
    path('admin/bid/<int:bid_id>/delete/', views.delete_bid_action, name='delete_bid'),
    path('admin/add-player/', views.admin_add_player, name='admin_add_player'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('all-players/', views.all_players_database, name='all_players'),
    path('profile/', views.team_profile, name='team_profile'),
    path('profile/edit-username/', views.edit_username, name='edit_username'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('team/<int:team_id>/', views.team_profile, name='team_profile_by_id'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login', http_method_names=['get', 'post', 'options']), name='logout'),
    path('', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)