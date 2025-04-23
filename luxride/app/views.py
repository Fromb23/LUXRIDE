from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.urls import reverse
from .forms import CarForm
from datetime import datetime
from django.http import HttpResponse
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

    current_step = request.user.current_step
    print(f"current_step: {current_step}")
    context = {
        'borrowed_car': True,
        'current_step': current_step,
        'step_range': range(1, 6),
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
def admin_dashboard(request):
    available_cars_count = 0
    borrowed_cars_count = 0
    pending_borrows_count = 0
    total_revenue = 0

    available_cars_count = BorrowedCar.objects.filter(
        status='available').count()

    borrowed_cars_count = BorrowedCar.objects.filter(status='borrowed').count()
    pending_borrows_count = BorrowedCar.objects.filter(
        status='pending').count()

    total_revenue = BorrowedCar.objects.aggregate(
        Sum('rental_price'))['rental_price__sum'] or 0

    recent_borrows = BorrowedCar.objects.order_by('-borrow_date')[:5]

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
        return redirect('manage_cars')


def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'dashboard/partials/car_details.html', {'car': car})


def get_selected_car(user, session):
    if user.selected_car_id:
        return user.selected_car

    car_id = session.get('car_id')
    if car_id:
        try:
            car = Car.objects.get(id=car_id)
            user.selected_car = car
            user.save()
            return car
        except Car.DoesNotExist:
            return None

    return None


def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})


def borrowed_logs(request):
    borrowed_cars = BorrowedCar.objects.all()
    return render(request, 'dashboard/borrowed_cars.html', {'borrowed_cars': borrowed_cars})


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


@require_POST
def step_control_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    step = int(request.POST.get('step', 0))
    lock = request.POST.get('lock', 'false') == 'true'

    user = request.user

    if step > user.current_step:
        user.current_step = step

    if lock:
        user.locked_steps = getattr(user, 'locked_steps', []) + [step]

    user.save()

    return JsonResponse({'success': True, 'current_step': user.current_step})


def user_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    query_car_id = request.GET.get('car_id')
    current_step = int(request.GET.get('step', user.current_step))
    car = None

    if query_car_id:
        car_instance = Car.objects.filter(id=query_car_id).first()
        if car_instance:
            user.selected_car = car_instance
            user.save()
            request.session['car_id'] = car_instance.id

    car = get_selected_car(user, request.session)

    if current_step == 2 and not car:
        return redirect(f"{reverse('user_dashboard')}?step=1&error=No+car+selected.")

    if current_step > user.current_step:
        user.current_step = current_step
        user.save()

    rental_price = car.rental_price if car else 0
    days = request.GET.get('days', 1)
    total_amount = rental_price * int(days) if car else 0
    print(f"Total amount: {total_amount}")
    borrowed_car = BorrowedCar.objects.filter(user=user).first()
    is_borrowed = borrowed_car.is_borrowed() if borrowed_car else False

    # === Navigation button logic ===
    step_range = range(1, 6)
    show_prev = current_step > 1
    hide_next = current_step in [1, 2, 4]
    show_next = (current_step < step_range[-1]) and not hide_next
    disable_next = False

    return render(request, 'dashboard/user_dashboard.html', {
        'borrowed_car': borrowed_car,
        'current_step': current_step,
        'step_range': step_range,
        'is_borrowed': is_borrowed,
        'cars': Car.objects.all(),
        'car': car,
        'show_prev': show_prev,
        'show_next': show_next,
        'hide_next': hide_next,
        'disable_next': disable_next,
        'days_range': range(1, 16),
        'total_amount': total_amount,
    })


def update_status(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            car.status = status
            car.save()
            messages.success(request, 'Car status updated successfully.')
        else:
            messages.error(request, 'No status provided.')
        return redirect('manage_cars')

    return render(request, 'dashboard/update_status.html', {'car': car})


# car application steps


def dashboard_step1(request):
    print("Step 1 view called")
    step = int(request.GET.get('step', 1))

    if request.method == 'POST' and step == 1:
        driving_license_no = request.POST.get('driving_license_no')

        # First try to get car_id from session
        car_id = request.session.get('car_id')

        # If not in session, try from user.selected_car
        if not car_id and request.user.is_authenticated and hasattr(request.user, 'selected_car'):
            car_id = request.user.selected_car.id

        if not car_id:
            return redirect(f"{reverse('user_dashboard')}?step=1&error=No+car+selected.")

        try:
            car = Car.objects.get(id=car_id)
            print(f"Car found: {car.model}")
        except Car.DoesNotExist:
            return redirect(f"{reverse('user_dashboard')}?step=1&error=Car+not+found.")

        if not driving_license_no:
            return redirect(f"{reverse('user_dashboard')}?step=1&error=All+fields+are+required.")

        return redirect(reverse('user_dashboard') + '?step=2')

    return render(request, 'dashboard/steps/step1.html', {'current_step': step})


def dashboard_step2(request):
    print("Step 2 view called")
    step = int(request.GET.get('step', 2))

    if request.method == 'POST' and step == 2:
        car_id = request.session.get('car_id')

        if not car_id:
            return redirect(f"{reverse('user_dashboard')}?step=1&error=No+car+selected.")

        try:
            car = Car.objects.get(id=car_id)
            print(f"Car found: {car.model}")
        except Car.DoesNotExist:
            return redirect(f"{reverse('user_dashboard')}?step=1&error=Car+not+found.")

        # Process the form data here
        # For example, save it to the database or perform any other action

        return redirect(reverse('user_dashboard') + '?step=3')

    return render(request, 'dashboard/steps/step2.html', {'current_step': step})


@csrf_exempt
@login_required
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        try:
            phone = request.POST.get('phone_number')
            car_id = request.POST.get('car_id')
            car = Car.objects.get(id=car_id)

            if not phone:
                raise ValueError("Phone number is required")

            user = request.user
            user.payment_status = CustomUser.PaymentStatus.PENDING
            user.save()

            return redirect(f"{reverse('user_dashboard')}?step=3")

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=405)


@csrf_exempt
@login_required
def process_card_payment(request):
    if request.method == 'POST':
        print("Card payment processed.")
        request.user.payment_status = 'pending'
        request.user.save()
    return redirect(f"{reverse('user_dashboard')}?step=3")


@login_required
def agree_terms(request):
    if not request.user.has_agreed_terms:
        request.user.has_agreed_terms = True
        request.user.save()

    return redirect('/dashboard/?step=5')


@login_required
def finalize_booking(request):
    if request.method == 'POST':
        car_id = request.user.selected_car_id

        if not car_id:
            return HttpResponseBadRequest("Car ID not found.")

        car = get_object_or_404(Car, id=car_id)

        BorrowedCar.objects.create(
            user=request.user,
            car=car,
            rental_price=car.rental_price,
            status='pending'
        )

        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('home')
