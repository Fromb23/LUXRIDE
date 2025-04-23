from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('none', 'No Car Borrowed'),
        ('pending', 'Pending'),
        ('waiting', 'Waiting Verification'),
        ('borrowed', 'Borrowed'),
    ]
    full_name = models.CharField(max_length=100, default="Unknown")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True)
    driving_license_no = models.CharField(max_length=50, unique=True)
    is_superuser = models.BooleanField(default=False)
    current_step = models.PositiveIntegerField(
        default=1, null=True, blank=True)
    has_agreed_terms = models.BooleanField(default=False)
    selected_car = models.ForeignKey(
        'Car', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='none',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'driving_license_no', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.current_step = None
        super(CustomUser, self).save(*args, **kwargs)

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'

    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )


class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('pending', 'Pending'),
    ]
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='media/car_images/', null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='available')
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=30, default='Unknown')

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class BorrowedCar(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('pending', 'Pending'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.user.full_name} borrowed {self.car.make} {self.car.model}"

    def is_borrowed(self):
        """Check if the car is currently borrowed."""
        return self.return_date is None
