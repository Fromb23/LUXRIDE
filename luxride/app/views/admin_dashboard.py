from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from ..models import BorrowedCar, BorrowCarHistory, Car, CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login
from ..forms import CarForm


@login_required
def dashboard(request):
    available_cars_count = BorrowedCar.objects.filter(
        status='available').count()
    borrowed_cars_count = BorrowedCar.objects.filter(status='borrowed').count()
    pending_borrows_count = BorrowedCar.objects.filter(
        status='pending').count()

    total_revenue = BorrowedCar.objects.aggregate(
        Sum('rental_price')
    )['rental_price__sum'] or 0

    # Get recent borrows from history
    recent_borrows = BorrowCarHistory.objects.order_by('-borrowed_date')[:5]

    # Ongoing borrows (still active)
    ongoing_borrows = BorrowedCar.objects.filter(status='borrowed')[:5]

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


def manage_cars(request):
    cars = Car.objects.all()
    for car in cars:
        print(car.image)
        print(car.image.url)
    return render(request, 'dashboard/manage_cars.html', {'cars': cars})


def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car created successfully.')
            return redirect('admin_dashboard')
    else:
        form = CarForm()
    return render(request, 'dashboard/create_car.html', {'form': form})


def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully.')
            return redirect('manage_cars')
    else:
        form = CarForm(instance=car)

    return render(request, 'dashboard/edit_car.html', {'form': form, 'car': car})


def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car deleted successfully.')
        return redirect('manage-cars')


def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'dashboard/partials/car_details.html', {'car': car})


def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})


def borrowed_logs(request):
    borrowed_cars = BorrowedCar.objects.all()
    print(f"Borrowed cars: {borrowed_cars}")
    statuses = [choice[0] for choice in BorrowedCar.STATUS_CHOICES]

    current_statuses = {}
    for borrowed_car in borrowed_cars:
        current_statuses[borrowed_car.id] = borrowed_car.status

    return render(request, 'dashboard/borrowed_cars.html', {
        'borrowed_cars': borrowed_cars,
        'statuses': statuses,
        'current_statuses': current_statuses
    })


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
