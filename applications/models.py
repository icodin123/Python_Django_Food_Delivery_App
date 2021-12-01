from django.db import models
from django import template

register = template.Library()

# Enum for Request Types
PROFILE_CHANGE = 'PR'
SCHEDULE_CHANGE = 'SC'
PAIRING_CHANGE = 'PA'
OTHER_CHANGE = 'O'

REQUEST_TYPES = [
    (PROFILE_CHANGE, 'Profile'),
    (SCHEDULE_CHANGE, 'Schedule'),
    (PAIRING_CHANGE, 'Pairing'),
    (OTHER_CHANGE, 'Other'),
]

# Enum for Application Reviews Type
PROGRAM_APPLICATION = 'PR'
RESTAURANT_APPLICATION = 'RE'

APPLICATION_TYPES = [
    (PROGRAM_APPLICATION, 'Program'),
    (RESTAURANT_APPLICATION, 'Restaurant')
]

# Enum for Request Review Status
PENDING = 'P'
APPROVED = 'A'
REJECTED = 'R'

REQUEST_REVIEW_STATUS = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
]

class MealHistory(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    restaurant_id = models.ForeignKey('profiles.Restaurant', on_delete=models.CASCADE, null=True)
    program_id = models.ForeignKey('profiles.Program', on_delete=models.CASCADE, null=True)
    meals = models.IntegerField(default=0)

class RequestReview(models.Model):
    request_id = models.ForeignKey('applications.Request', related_name="review",\
                                on_delete=models.DO_NOTHING)

    admin_id = models.ForeignKey('profiles.UserClass', related_name='reviews',\
                                on_delete=models.DO_NOTHING, null=True)

    created_at = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=200, null=True)

    status = models.CharField(max_length=20,\
                            choices=REQUEST_REVIEW_STATUS,\
                            default=PENDING)

    def __str__(self):
        return self.status

# request applicaiton for schools
class Request(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey('profiles.UserClass', related_name="request", on_delete=models.DO_NOTHING)

    schedule_id = models.ForeignKey('profiles.Schedule', on_delete=models.DO_NOTHING, null=True)

    request_change = models.CharField(max_length=200, null=True)
    current_request_review_id = models.ForeignKey('applications.RequestReview',\
                                                related_name="request",\
                                                on_delete=models.CASCADE,\
                                                null=True)
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPES,
        default=PROFILE_CHANGE,
    )

    def __str__(self):
        return 'id: ' + str(self.id) + 'type: ' + str(self.request_type)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return 'success'

    def get_type(self):
        if self.request_type == 'PR':
            return 'Profile Change'
        elif self.request_type == 'SC':
            return 'Schedule Change'
        elif self.request_type == 'PA':
            return 'Pairing Change'
        else:
            return 'Other'


    class Meta:
        ordering = ["-created_at"]

POSSIBLE_STATUS = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
]

class ApplicationReview(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=APPLICATION_TYPES,
        default=PROGRAM_APPLICATION,
    )

    model_id = models.ForeignKey('profiles.UserClass', on_delete=models.DO_NOTHING, related_name='application_review_user')
    admin_by_id = models.ForeignKey('profiles.UserClass', on_delete=models.DO_NOTHING, null=True, related_name='application_review_admin')
    status = models.CharField(
        max_length=20,
        choices=POSSIBLE_STATUS,
        default=PENDING,
    )
    comments = models.CharField(max_length=200)

    def get_type(self):
        if self.type == 'PR':
            return "Program Application"
        else:
            return "Restaurant Application"


class PairingsManager(models.Manager):
    """Manager for Note class"""

    def create_pairing(self, schedule_id, program_id=None, restaurant_id=None, meals=0):
        new_pairing = Pairings()
        new_pairing.schedule_id = schedule_id
        if program_id:
            new_pairing.program_id = program_id
        if restaurant_id:
            new_pairing.restaurant_id = restaurant_id

        new_pairing.meals = meals

        new_pairing.save(using=self._db)
        return new_pairing


class Pairings(models.Model):
    """Model for pairings between programs and restaurants."""
    created_at = models.DateTimeField(auto_now=True)
    restaurant_id = models.ForeignKey('profiles.Restaurant', on_delete=models.CASCADE, null=True)
    program_id = models.ForeignKey('profiles.Program', on_delete=models.CASCADE, null=True)
    schedule_id = models.ForeignKey('profiles.Schedule', on_delete=models.DO_NOTHING, null=True)
    meals = models.IntegerField(default=0)

# Enum for Notification Types
APPLICATION = 'A'
REQUEST = 'R'
CREATE_USER = 'C'

NOTIFICATION_TYPES = [
    (APPLICATION, 'Application'),
    (REQUEST, 'Request'),
    (CREATE_USER, 'Create_User')
]

class Notification(models.Model):
    """Model for notifications for users"""
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default=APPLICATION,
    )
    application = models.ForeignKey('applications.ApplicationReview', on_delete=models.CASCADE, null=True)
    request = models.ForeignKey('applications.Request', on_delete=models.CASCADE, null=True)
    basic_user = models.ForeignKey('profiles.UserClass', on_delete=models.CASCADE, null=True)
    is_dismissed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at) + "--- dismissed:" + str(self.is_dismissed)

    def content(self):
        if self.notification_type == 'A':
            return'Application from {} {}'.format(self.application.model_id.first_name, self.application.model_id.last_name)
        elif self.notification_type == 'R':
            return 'Request from {} {}'.format(self.request.user_id.first_name, self.request.user_id.last_name)
        else:
            return '{} {} has signed up'.format(self.basic_user.first_name, self.basic_user.last_name)
