from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import json
import datetime
from django.urls import reverse, reverse_lazy
from .forms import CarForm, BorrowedCarForm
from django.utils import timezone
from django.http import HttpResponse
from .models import CustomUser, BorrowedCar, Car, BorrowCarHistory
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetConfirmView


def home(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'auth/login.html')


def register_view(request):
    return render(request, 'auth/create_user.html')


def is_regular_user(user):
    return user.is_authenticated and not user.is_superuser


@login_required
@user_passes_test(is_regular_user)
def user_dashboard(request):
    if not is_regular_user(request.user):
        return redirect('admin_dashboard')

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
    print("Car details view called")
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


@require_http_methods(["GET", "POST"])
def user_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        return handle_step_control(request)

    return handle_dashboard_view(request)


def handle_step_control(request):
    """Handle step control POST requests"""
    user = request.user
    try:
        step = int(request.POST.get('step', 0))
        lock = request.POST.get('lock', 'false') == 'true'
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    if step > user.current_step:
        user.current_step = step

    locked_steps = getattr(user, 'locked_steps', [])
    if lock and step not in locked_steps:
        locked_steps.append(step)
    elif not lock and step in locked_steps:
        locked_steps.remove(step)
    user.locked_steps = locked_steps

    user.save()
    return JsonResponse({
        'success': True,
        'current_step': user.current_step,
        'locked_steps': locked_steps
    })


@login_required
def start_new_booking(request):
    """Start a new booking by resetting the user's current step"""
    user = request.user
    user.current_step = 0
    user.has_agreed_terms = False
    user.locked_steps = []
    user.selected_car_id = None
    user.save()
    print(f"user selected car id after reset: {user.selected_car_id}")

    # Clear the session car_id
    request.session.pop('car_id', None)
    return redirect('user_dashboard')


def get_rental_history(user):
    """Get the rental history of the user"""
    return BorrowCarHistory.objects.filter(user=user).order_by('-borrowed_date')


def handle_dashboard_view(request):
    user = request.user

    if not hasattr(user, 'current_step'):
        raise Http404("You haven't started any step.")

    try:
        requested_step = int(request.GET.get('step', user.current_step))
    except (TypeError, ValueError):
        requested_step = user.current_step

    # Allow step 0 as default
    requested_step = max(0, min(requested_step, 5))
    locked_steps = getattr(user, 'locked_steps', [])

    query_car_id = request.GET.get('car_id')
    car = None
    if query_car_id:
        car_instance = Car.objects.filter(id=query_car_id).first()
        if car_instance and (not user.selected_car or user.selected_car.id != car_instance.id):
            user.current_step = 0
            user.locked_steps = []
            user.has_agreed_terms = False
            user.selected_car = car_instance
            user.save()
            request.session['car_id'] = car_instance.id

    car = get_selected_car(user, request.session)

    if requested_step > 0:
        if requested_step == 2 and not car:
            return HttpResponseForbidden("Access to step 2 denied. No car selected.")

        if requested_step > user.current_step and requested_step in locked_steps:
            raise Http404("Step not allowed.")

        if requested_step <= user.current_step + 1 and requested_step not in locked_steps:
            if requested_step > user.current_step:
                user.current_step = requested_step
                user.save()
        else:
            return redirect(f"{reverse('user_dashboard')}?step={user.current_step}&error=Step+not+allowed")

    # Pricing
    rental_price = car.rental_price if car else 0
    days = int(request.GET.get('days', 1))
    total_amount = rental_price * days if car else 0

    borrowed_car = BorrowedCar.objects.filter(user=user).first()
    print(f"Borrowed car by user: {borrowed_car}")
    is_borrowed = borrowed_car.is_borrowed() if borrowed_car else False

    days_borrowed = user.days_borrowed
    if days_borrowed < 1:
        days_borrowed = 1

    total_cost = days_borrowed * \
        (user.selected_car.rental_price if user.selected_car else 0)

    return_date = request.user.return_date
    if return_date:
        return_datetime = datetime.datetime.combine(
            return_date, datetime.time.min)
        return_timestamp = return_datetime.timestamp()
    else:
        return_timestamp = None

    retal_history = None
    if borrowed_car or is_borrowed is not None:
        retal_history = get_rental_history(user)
        for history in retal_history:
            print(f"Rental history status: {history.status}")

    # Navigation logic
    step_range = range(1, 6)
    show_prev = requested_step > 0
    hide_next = requested_step in [2, 4]
    show_next = (
        requested_step > 0 and not hide_next and
        requested_step < 5 and
        (requested_step < user.current_step or requested_step == 3)
    )

    return render(request, 'dashboard/user_dashboard.html', {
        'borrowed_car': borrowed_car,
        'current_step': requested_step,
        'max_reached_step': user.current_step,
        'step_range': step_range,
        'is_borrowed': is_borrowed,
        'cars': Car.objects.all(),
        'car': car,
        'show_prev': show_prev,
        'show_next': show_next,
        'hide_next': hide_next,
        'days_range': range(1, 16),
        'total_amount': total_amount,
        'total_cost': total_cost,
        'return_date':  return_timestamp,
        'rental_history': retal_history,
        'resume': request.GET.get('resume') == 'true',
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


def update_borrowed_car_status(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            borrowed_car = BorrowedCar.objects.get(pk=pk)
            borrowed_car.status = status
            borrowed_car.save()
            car = borrowed_car.car
            car.status = status
            car.available = False if status == 'borrowed' or status == 'pending' else True
            car.save()

            borrower = borrowed_car.user
            if status == 'borrowed':
                borrower.status = 'borrowed'
            elif status == 'available':
                borrower.status = 'available'
            elif status == 'pending':
                borrower.status = 'pending'
            borrower.save()

            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


# car application steps


def dashboard_step1(request):
    print("Step 1 view called")
    step = int(request.GET.get('step', 1))

    if request.method == 'POST' and step == 1:
        driving_license_no = request.POST.get('driving_license_no')

        car_id = request.session.get('car_id')

        if not car_id and request.user.is_authenticated and hasattr(request.user, 'selected_car'):
            car_id = request.user.selected_car_id

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
            return_date_str = request.POST.get('return_date')
            print(f"Return date: {return_date_str}")

            if not return_date_str:
                raise ValueError("Return date is required")

            # Convert the return_date string to a date object
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
            borrowed_date = timezone.now().date()

            # Calculate number of days
            days_borrowed = (return_date - borrowed_date).days
            if days_borrowed < 1:
                days_borrowed = 1

            user = request.user
            user.payment_status = CustomUser.PaymentStatus.PENDING
            user.borrowed_date = borrowed_date
            user.return_date = return_date
            user.days_borrowed = days_borrowed
            user.status = 'pending'
            user.save()

            # Store in session if needed
            request.session['days_borrowed'] = days_borrowed

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
        current_step = request.user.current_step
        current_step = 0
        request.user.current_step = current_step
        request.user.save()

        if not car_id:
            return HttpResponseBadRequest("Car ID not found.")

        car = get_object_or_404(Car, id=car_id)

        borrowed_car = BorrowedCar.objects.create(
            user=request.user,
            car=car,
            rental_price=car.rental_price,
            status='pending'
        )
        borrowed_car.save()

        borrowed_car_history = BorrowCarHistory.objects.create(
            user=request.user,
            car=car,
            borrowed_date=timezone.now(),
            return_date=request.user.return_date,
            status='pending'
        )
        borrowed_car_history.save()

        return redirect('user_dashboard')


def update_car_status(request, car_id):
    borrowed_car = get_object_or_404(BorrowedCar, id=car_id)

    if request.method == 'POST':
        form = BorrowedCarForm(request.POST, instance=borrowed_car)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BorrowedCarForm(instance=borrowed_car)

    return render(request, 'dashboard/borrowed_cars.html', {'form': form, 'borrowed_car': borrowed_car})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    from django.contrib.auth.forms import SetPasswordForm
    form_class = SetPasswordForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('home')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
