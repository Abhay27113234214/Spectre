from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator

# Create your models here.

class Company(models.Model):
    INDUSTRY_CHOICES = (
        ('', '---------'),
        ('TECH', 'Technology'),
        ('FIN', 'Finance'),
        ('HEALTH', 'Healthcare'),
        ('MANU', 'Manufacturing'),
        ('RETAIL', 'Retail/E-commerce'),
        ('PROF_SVC', 'Professional Services'),
        ('EDU', 'Education'),
        ('ENERGY', 'Energy'),
        ('TRANS', 'Transportation & Logistics'),
        ('REALEST', 'Real Estate & Construction'),
        ('HOSP', 'Hospitality'),
        ('MEDIA', 'Media & Entertainment'),
        ('AGRI', 'Agriculture'),
        ('NONPROF', 'Non-Profit'),
        ('GOV', 'Government'),
        ('OTHER', 'Other'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.URLField(max_length=300, blank=True)
    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(regex=r"^(\+?91)?\d{10}$")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    industry = models.CharField(
        max_length=20,
        choices=INDUSTRY_CHOICES,
        blank=True, 
        null=True   
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class AppUserManager(BaseUserManager):
    def create_user(self, email, full_name, company, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field is mandatory!')
        if company is None and not extra_fields.get('is_superuser'):
            raise ValueError('Non-superuser User must be associated with a company!')
        if isinstance(company, int):
            company = Company.objects.get(id=company)
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            full_name = full_name,
            company = company,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, company=None , password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Superusers must have a password.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('company') is not True:
            pass
        return self.create_user(email=email, full_name=full_name, password=password, **extra_fields)



class AppUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Company Admin'),
        ('MEMBER', 'Employee Member'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r"^(\+91)?\d{10}$")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, default='MEMBER', choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = None
    objects = AppUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email