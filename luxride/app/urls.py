from django.urls import path, reverse_lazy
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from .forms import CustomPasswordResetForm, PasswordResetForm
from .views import CustomPasswordResetConfirmView

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
    path('start-new-booking/', views.start_new_booking, name='start_new_booking'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('cars/<int:car_id>/status/', views.update_status,
         name='update_status'),
    path('dashboard/car_details/<int:car_id>/',
         views.car_details, name='car_details'),
    path('admin/dashboard/borrowed-car/<int:car_id>/edit/',
         views.update_car_status, name='update_car_status'),

    # user management
    path('admin/dashboard/users/',
         views.manage_users, name='manage_users'),

    # borrowed logs
    path('admin/dashboard/borrowed-logs/',
         views.borrowed_logs, name='borrowed_logs'),
    path('admin/dashboard/reports/',
         views.generate_report, name='generate_report'),
    path('update-borrowed-car-status/<int:pk>/',
         views.update_borrowed_car_status, name='update_borrowed_car_status'),

    # steps for car application
    path('dashboard/step1', views.dashboard_step1, name='dashboard_step1'),
    path('dashboard/step2/', views.dashboard_step2, name='dashboard_step2'),

    # initiate mpesa payment
    path('initiate-mpesa-payment/',
         views.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('card-payment/', views.process_card_payment,
         name='process_card_payment'),
    path('agree-terms/', views.agree_terms, name='agree_terms'),
    path('finalize-booking/', views.finalize_booking, name='finalize_booking'),

    # Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             form_class=CustomPasswordResetForm,
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',

         CustomPasswordResetConfirmView.as_view(),
         #    success_url=reverse_lazy('password_reset_complete')

         name='password_reset_confirm'),

    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(

             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
