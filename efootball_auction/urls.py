from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from auction import views

urlpatterns = [
    path('admin/bid-view/', views.admin_bid_view, name='admin_bid_view'),
    path('admin/player-bids/<int:player_id>/', views.player_bid_detail, name='player_bid_detail'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)