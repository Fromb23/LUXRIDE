from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from ..models import CustomUser


def home(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'auth/login.html')


def register_view(request):
    return render(request, 'auth/create_user.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)

            if user.check_password(password):
                login(request, user)

                messages.success(request, 'Login successful.')

                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')

            else:
                return render(request, 'auth/login.html', {'error': 'Invalid credentials.'})
        except CustomUser.DoesNotExist:
            return render(request, 'auth/login.html', {'error': 'User does not exist.'})

    return render(request, 'auth/login.html')
