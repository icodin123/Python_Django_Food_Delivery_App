from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Enum for Admin
BASIC_ADMIN = 'ADMIN'
SUPER_ADMIN = 'SUPER'
MANAGER = 'MNGR'
DEVELOPER = 'DEV'
STAFF = 'STAFF'

ADMIN_ROLE_OPTIONS = [
    (BASIC_ADMIN, 'basic admin'),
    (SUPER_ADMIN, 'super admin'),
    (MANAGER, 'manager'),
    (DEVELOPER, 'developer'),
    (STAFF, 'stuff'),
]

PROGRAM = "PR"
RESTAURANT = "RE"

USER_TYPE_OPTIONS = [
    (PROGRAM, 'Program'),
    (RESTAURANT, 'Restaurant'),
]

PHONE = "PH"
EMAIL = "EM"

PREFERRED_CONTACT = [
    (PHONE, 'Phone'),
    (EMAIL, 'Email'),
]

ADMIN = "ADM"
BASIC_USER = "BSC"

USER_TYPES = [
    (ADMIN, 'Admin'),
    (BASIC_USER, 'Basic User'),
]

class UserClassManager(BaseUserManager):
    """Manager for User class"""

    # method for creatig admins, but not super admins
    def create_staffuser(self, last_name, first_name, email, password, role, phone_number=''):
        new_account = self.create_user(phone_number=phone_number, last_name=last_name, first_name=first_name,
                                    email=email, password=password)
        new_account.staff = True

        admin_object = AdminUser.objects.create(role=role)
        new_account.admin_object = admin_object
        new_account.user_type = ADMIN
        admin_object.save(using=self._db)

        new_account.save(using=self._db)
        return new_account

    def create_basic_user(self, type, last_name, first_name, email, password, phone_number=''):
        new_account = self.create_user(phone_number=phone_number, last_name=last_name, first_name=first_name,
                                    email=email, password=password)
        user_object = BasicUser.objects.create(type=type)
        new_account.user_object = user_object
        new_account.user_type = BASIC_USER

        user_object.save(using=self._db)
        new_account.save(using=self._db)

        return new_account

    # method for creating restaurants, schools, etc.
    def create_user(self, last_name, first_name, email, password, phone_number=''):
        new_account = self.model(email=self.normalize_email(email),)
        new_account.set_password(password)

        new_account.last_name = last_name
        new_account.first_name = first_name

        new_account.phone_number = phone_number

        new_account.save(using=self._db)
        return new_account

    # method for creating superadmins
    def create_superuser(self, last_name, first_name, email, password, phone_number=''):
        new_account = self.create_user(phone_number=phone_number, last_name=last_name, first_name=first_name,
                                    email=email, password=password)
        new_account.staff = True
        new_account.admin = True

        admin_object = AdminUser.objects.create(role=SUPER_ADMIN)
        new_account.admin_object = admin_object
        new_account.user_type = ADMIN
        admin_object.save(using=self._db)

        new_account.save(using=self._db)
        return new_account

    # add any required fields here other than email and password
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


class UserClass(AbstractBaseUser):
    """Class for general user - can be basic user or admin"""
    phone_number = models.CharField(verbose_name='phone number', max_length=255, unique=False, default='')
    active = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    email = models.EmailField(verbose_name='email', max_length=255, unique=True, )
    last_name = models.CharField(verbose_name='last name', max_length=255, unique=False, )
    first_name = models.CharField(verbose_name='first name', max_length=255, unique=False, )
    objects = UserClassManager()
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    image = models.CharField(verbose_name='user image', max_length=255, unique=False, default='defaultIcon.png')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default=BASIC_USER,
    )

    user_object = models.ForeignKey('profiles.BasicUser', on_delete=models.DO_NOTHING, null=True, related_name='basic_user_parent')
    admin_object = models.ForeignKey('profiles.AdminUser', on_delete=models.DO_NOTHING, null=True, related_name='admin_user_parent')

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
        return self.email

class AdminUser(models.Model):
    """Model for admin user data"""
    role = models.CharField(
        max_length=20,
        choices=ADMIN_ROLE_OPTIONS,
        default=STAFF,
    )

class BasicUser(models.Model):
    """Model for basic user data"""
    type = models.CharField(
        max_length=20,
        choices=USER_TYPE_OPTIONS,
        default=RESTAURANT,
    )

    preferred_contact = models.CharField(
        max_length=20,
        choices=PREFERRED_CONTACT,
        default=EMAIL,
    )

    position = models.CharField(verbose_name='position/title', max_length=255, unique=False, null=True)

    restaurant = models.ForeignKey('profiles.Restaurant', on_delete=models.CASCADE, null=True)
    program = models.ForeignKey('profiles.Program', on_delete=models.CASCADE, null=True)
    courier = models.ForeignKey('profiles.Courier', on_delete=models.CASCADE, null=True)

class Schedule(models.Model):
    monday_start = models.TimeField(auto_now=False, null=True, blank=True)
    monday_end = models.TimeField(auto_now=False, null=True, blank=True)
    tuesday_start = models.TimeField(auto_now=False, null=True, blank=True)
    tuesday_end = models.TimeField(auto_now=False, null=True, blank=True)
    wednesday_start = models.TimeField(auto_now=False, null=True, blank=True)
    wednesday_end = models.TimeField(auto_now=False, null=True, blank=True)
    thursday_start = models.TimeField(auto_now=False, null=True, blank=True)
    thursday_end = models.TimeField(auto_now=False, null=True, blank=True)
    friday_start = models.TimeField(auto_now=False, null=True, blank=True)
    friday_end = models.TimeField(auto_now=False, null=True, blank=True)
    saturday_start = models.TimeField(auto_now=False, null=True, blank=True)
    saturday_end = models.TimeField(auto_now=False, null=True, blank=True)
    sunday_start = models.TimeField(auto_now=False, null=True, blank=True)
    sunday_end = models.TimeField(auto_now=False, null=True, blank=True)

    def getSchedule(self):
        schedule = {}
        if self.monday_start:
            schedule['monday_start'] = self.monday_start.strftime("%-I:%M %p")
        else:
            schedule['monday_start'] = ''
        if self.monday_end:
            schedule['monday_end'] = self.monday_end.strftime("%-I:%M %p")
        else:
            schedule['monday_end'] = ''
        if self.tuesday_start:
            schedule['tuesday_start'] = self.tuesday_start.strftime("%-I:%M %p")
        else:
            schedule['tuesday_start'] = ''
        if self.tuesday_end:
            schedule['tuesday_end'] = self.tuesday_end.strftime("%-I:%M %p")
        else:
            schedule['tuesday_end'] = ''
        if self.wednesday_start:
            schedule['wednesday_start'] = self.wednesday_start.strftime("%-I:%M %p")
        else:
            schedule['wednesday_start'] = ''
        if self.wednesday_end:
            schedule['wednesday_end'] = self.wednesday_end.strftime("%-I:%M %p")
        else:
            schedule['wednesday_end'] = ''
        if self.thursday_start:
            schedule['thursday_start'] = self.thursday_start.strftime("%-I:%M %p")
        else:
            schedule['thursday_start'] = ''
        if self.thursday_end:
            schedule['thursday_end'] = self.thursday_end.strftime("%-I:%M %p")
        else:
            schedule['thursday_end'] = ''
        if self.friday_start:
            schedule['friday_start'] = self.friday_start.strftime("%-I:%M %p")
        else:
            schedule['friday_start'] = ''
        if self.friday_end:
            schedule['friday_end'] = self.friday_end.strftime("%-I:%M %p")
        else:
            schedule['friday_end'] = ''
        if self.saturday_start:
            schedule['saturday_start'] = self.saturday_start.strftime("%-I:%M %p")
        else:
            schedule['saturday_start'] = ''
        if self.saturday_end:
            schedule['saturday_end'] = self.saturday_end.strftime("%-I:%M %p")
        else:
            schedule['saturday_end'] = ''
        if self.sunday_start:
            schedule['sunday_start'] = self.sunday_start.strftime("%-I:%M %p")
        else:
            schedule['sunday_start'] = ''
        if self.sunday_end:
            schedule['sunday_end'] = self.sunday_end.strftime("%-I:%M %p")
        else:
            schedule['sunday_end'] = ''

        return schedule

class Restaurant(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(verbose_name='company name', max_length=255, unique=False, )
    main_contact = models.ForeignKey('profiles.UserClass', on_delete=models.DO_NOTHING, related_name="restaurant_object", null=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=255, unique=False, )
    schedule = models.ForeignKey('profiles.Schedule', on_delete=models.DO_NOTHING, null=True)
    meals = models.IntegerField()
    uber_eats = models.BooleanField(default=False)
    delivery_capacity = models.BooleanField(default=False)
    packaging = models.BooleanField(default=False)
    health_certificate = models.CharField(verbose_name='health certificate', max_length=255, unique=False, )
    address = models.CharField(verbose_name='address', max_length=255, unique=False, )
    coordinates = models.CharField(verbose_name='coordinates', max_length=255, unique=False, null=True)
    latitude = models.CharField(verbose_name='latitude', max_length=255, unique=False, null=True)
    longitude = models.CharField(verbose_name='longitude', max_length=255, unique=False, null=True)
    review = models.ForeignKey('applications.ApplicationReview', related_name='restaurants',
                            on_delete=models.DO_NOTHING, null=True)

class Program(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    program_name = models.CharField(verbose_name='program name', max_length=255, unique=False, )
    main_contact = models.ForeignKey('profiles.UserClass', on_delete=models.DO_NOTHING, related_name="program_object", null=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=255, unique=False, )
    schedule = models.ForeignKey('profiles.Schedule', on_delete=models.DO_NOTHING, null=True)
    meals = models.IntegerField(default=0, null=True)
    address = models.CharField(verbose_name='address', max_length=255, unique=False, )
    coordinates = models.CharField(verbose_name='address', max_length=255, unique=False, null=True)
    latitude = models.CharField(verbose_name='latitude', max_length=255, unique=False, null=True)
    longitude = models.CharField(verbose_name='longitude', max_length=255, unique=False, null=True)
    review = models.ForeignKey('applications.ApplicationReview', related_name="programs",
                            on_delete=models.DO_NOTHING, null=True)

class Courier(models.Model):
    created_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True)

    def __str__(self):
        return self.user.username
