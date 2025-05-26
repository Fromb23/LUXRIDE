from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    from django.contrib.auth.forms import SetPasswordForm
    form_class = SetPasswordForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
