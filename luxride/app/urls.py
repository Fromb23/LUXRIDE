from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import auth, admin_dashboard, client_dashboard, reports, CustomPasswordResetConfirmView
from .forms import CustomPasswordResetForm


urlpatterns = [
    path('', auth.home, name='home'),
    path('auth/login/', auth.login_view, name='login'),
    path('auth/logout/', auth.logout_view, name='logout'),
    path('auth/register/', auth.register_view, name='register'),
    path('admin/dashboard/', admin_dashboard.dashboard, name='admin_dashboard'),
    path('admin/dashboard/main-content/', admin_dashboard.admin_main_content,
         name='admin_main_content'),
    path('dashboard/', client_dashboard.user_dashboard_view, name='user_dashboard'),

    # car management
    path('admin/dashboard/cars/', admin_dashboard.manage_cars, name='manage-cars'),
    path('dashboard/cars/create/', admin_dashboard.create_car, name='create_car'),
    path('start-new-booking/', client_dashboard.start_new_booking,
         name='start_new_booking'),
    path('cars/<int:car_id>/edit/', admin_dashboard.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/',
         admin_dashboard.delete_car, name='delete_car'),
    path('cars/<int:car_id>/status/', client_dashboard.update_status,
         name='update_status'),
    path('dashboard/car_details/<int:car_id>/',
         admin_dashboard.car_details, name='car_details'),
    path('admin/dashboard/borrowed-car/<int:car_id>/edit/',
         client_dashboard.update_car_status, name='update_car_status'),

    # user management
    path('admin/dashboard/users/',
         admin_dashboard.manage_users, name='manage_users'),

    # borrowed logs
    path('admin/dashboard/borrowed-logs/',
         admin_dashboard.borrowed_logs, name='borrowed_logs'),
    path('admin/dashboard/reports/',
         reports.generate_report, name='generate_report'),
    path('update-borrowed-car-status/<int:pk>/',
         client_dashboard.update_borrowed_car_status, name='update_borrowed_car_status'),

    # steps for car application
    path('dashboard/step1', client_dashboard.dashboard_step1, name='dashboard_step1'),
    path('dashboard/step2/', client_dashboard.dashboard_step2,
         name='dashboard_step2'),

    # initiate mpesa payment
    path('initiate-mpesa-payment/',
         client_dashboard.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('card-payment/', client_dashboard.process_card_payment,
         name='process_card_payment'),
    path('agree-terms/', client_dashboard.agree_terms, name='agree_terms'),
    path('finalize-booking/', client_dashboard.finalize_booking,
         name='finalize_booking'),

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
