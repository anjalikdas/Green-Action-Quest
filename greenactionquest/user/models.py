from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Add a related_name for groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users'
    )

    # Add a related_name for user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_users'
    )

    def __str__(self):
        return self.email

class CarbonFootprintData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # Travel Emissions Data
    travel_mode = models.CharField(max_length=50, choices=[('car', 'Car'), ('bus', 'Bus'), ('train', 'Train'), ('flight', 'Flight')])
    distance_traveled = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fuel_efficiency = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    number_of_passengers = models.PositiveIntegerField(default=1)
    aircraft_type = models.CharField(max_length=50, blank=True, null=True)
    
    # Dietary Emissions Data
    diet_type = models.CharField(max_length=50, choices=[('omnivorous', 'Omnivorous'), ('vegetarian', 'Vegetarian'), ('vegan', 'Vegan')])
    food_origin = models.CharField(max_length=50, choices=[('local', 'Local'), ('imported', 'Imported')])
    
    # Waste Emissions Data
    total_waste_generated = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    recyclable_materials_recycled = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    organic_waste_composted = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Home Energy Emissions Data
    electricity_consumption = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    heating_cooling_energy_consumption = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    household_size = models.PositiveIntegerField(default=1)
    renewable_energy_capacity = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    electricity_source = models.CharField(max_length=50, choices=[
        ('coal', 'Coal'),
        ('natural_gas', 'Natural Gas'),
        ('renewable', 'Renewable Energy'),
        ('other', 'Other'),
    ], blank=True, null=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carbon Footprint Data for {self.user.first_name}'

