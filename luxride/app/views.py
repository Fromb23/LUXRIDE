from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/create_user.html')

def user_dashboard(request):
    context = {
    'borrowed_car': True,
    'current_step': 2,
    'step_range': range(1, 7),
}
    return render(request, 'dashboard/user_dashboard.html', context)

def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')