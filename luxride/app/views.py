from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpRequest
from .models import CustomUser, BorrowedCar, Car
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login, logout


def home(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'auth/login.html')


def register_view(request):
    return render(request, 'auth/create_user.html')


@login_required
def user_dashboard(request):
    context = {
        'borrowed_car': True,
        'current_step': 2,
        'step_range': range(1, 7),
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
def admin_dashboard(request):
    available_cars_count = 0
    borrowed_cars_count = 0
    pending_borrows_count = 0
    total_revenue = 0

    available_cars_count = BorrowedCar.objects.filter(
        status='Available').count()
    borrowed_cars_count = BorrowedCar.objects.filter(
        current_step=1).count()

    pending_borrows_count = BorrowedCar.objects.filter(
        current_step=2).count()

    total_revenue = BorrowedCar.objects.aggregate(
        Sum('rental_price'))['rental_price__sum'] or 0

    recent_borrows = BorrowedCar.objects.order_by('-borrow_date')[:5]

    ongoing_borrows = BorrowedCar.objects.filter(current_step=1)[:5]

    context = {
        'available_cars_count': available_cars_count,
        'borrowed_cars_count': borrowed_cars_count,
        'pending_borrows_count': pending_borrows_count,
        'total_revenue': total_revenue,
        'recent_borrows': recent_borrows,
        'ongoing_borrows': ongoing_borrows,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


def admin_main_content(request):
    return render(request, 'dashboard/admin_main_content.html')


def register_view(request):
    print("Register view called")
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == "register_form":
            print("Register form submitted")
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            driving_license_no = request.POST.get('driving_license_no')

            if password != confirm_password:
                print("Passwords do not match")
                return render(request, 'auth/create_user.html', {'error': 'Passwords do not match.'})

            hashed_password = make_password(password)
            CustomUser.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=hashed_password,
                driving_license_no=driving_license_no
            )

            return render(request, 'auth/login.html', {'success': 'User created successfully.'})

    return render(request, 'auth/create_user.html')


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


def user_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    borrowed_car = BorrowedCar.objects.filter(user=request.user).first()

    current_step = int(request.GET.get('step', 1))
    step_range = range(1, 8)
    print(f"borrowed_car: {borrowed_car}")
    print(list(step_range))

    if borrowed_car and borrowed_car.current_step != current_step:
        borrowed_car.current_step = current_step
        borrowed_car.save()

    is_borrowed = borrowed_car.is_borrowed() if borrowed_car else False
    return render(request, 'dashboard/user_dashboard.html', {
        'borrowed_car': borrowed_car,
        'current_step': current_step,
        'step_range': step_range,
        'is_borrowed': is_borrowed,
    })


def logout_view(request):
    logout(request)
    return redirect('home')
