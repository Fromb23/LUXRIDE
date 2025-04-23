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

    # steps for car application
    path('dashboard/step1', views.dashboard_step1, name='dashboard_step1'),
    path('dashboard/step2/', views.dashboard_step2, name='dashboard_step2'),

    # initiate mpesa payment
    path('initiate-mpesa-payment/',
         views.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('card-payment/', views.process_card_payment,
         name='process_card_payment'),
    path('agree-terms/', views.agree_terms, name='agree_terms'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
