from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from auction import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('admin/bid-view/', views.admin_bid_view, name='admin_bid_view'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)