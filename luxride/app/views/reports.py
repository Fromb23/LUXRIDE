from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from ..models import BorrowedCar
from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@login_required
def generate_report(request):
    borrowers = BorrowedCar.objects.all()
    total_revenue = sum(b.rental_price for b in borrowers)
    page_objects = paginate_queryset(request, borrowers, per_page=5)
    return render(request, 'dashboard/generate_reports.html', {'borrowers': page_objects, 'total_revenue': total_revenue})
