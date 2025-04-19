from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/main-content/', views.admin_main_content,
         name='admin_main_content'),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),

    # car management
    path('admin/dashboard/cars/', views.manage_cars, name='manage-cars'),
    path('dashboard/cars/create/', views.create_car, name='create_car'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('cars/<int:car_id>/status/', views.update_status,
         name='update_status'),
    path('dashboard/car_details/<int:car_id>/',
         views.car_details, name='car_details'),

    # user management
    path('admin/dashboard/users/',
         views.manage_users, name='manage_users'),

    # borrowed logs
    path('admin/dashboard/borrowed-logs/',
         views.borrowed_logs, name='borrowed_logs'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
