import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homepage.settings')
import django
django.setup()
import random
from profiles.models import Schedule, AdminUser, BasicUser, UserClass
from profiles.models import Restaurant, Program
from applications.models import Request, ApplicationReview, RequestReview, Pairings, Notification,MealHistory
from faker import Faker

fakegen = Faker()
resource_names=['help1', 'assist1', 'help2', 'help3']
sizes = [0, 2.3, 4, 0]
descriptions =['desc1', 'thanks', 'desc2', 'df']

def populate_Schedule(N=10):
    for entry in range(N):

        if random.randint(1, 1000) % 2:
            monday_start = random.randint(11, 14)
            monday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            tuesday_start = random.randint(11, 14)
            tuesday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            wednesday_start = random.randint(11, 14)
            wednesday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            thursday_start = random.randint(11, 14)
            thursday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            friday_start = random.randint(11, 14)
            friday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            saturday_start = random.randint(11, 14)
            saturday_end = random.randint(14, 16)

        if random.randint(1, 1000) % 2:
            sunday_start = random.randint(11, 14)
            sunday_end = random.randint(14, 16)

        schedule = Schedule.objects.get_or_create(monday_start=monday_start,\
                                                monday_end=monday_end,\
                                                tuesday_start=tuesday_start,\
                                                tuesday_end=tuesday_end,\
                                                wednesday_start=wednesday_start,\
                                                wednesday_end=wednesday_end,\
                                                thursday_start=thursday_start,\
                                                thursday_end=thursday_end,\
                                                friday_start=friday_start,\
                                                friday_end=friday_end,\
                                                saturday_start=saturday_start,
                                                saturday_end=saturday_end,\
                                                sunday_start=sunday_start,\
                                                sunday_end=sunday_end)[0]
        schedule.save()


def populate_single_restaurant_Schedule():

    monday_start = tuesday_start = wednesday_start = '15:00'
    thursday_start = friday_start = '15:00'

    monday_end = tuesday_end = wednesday_end = saturday_start = sunday_start = None
    thursday_end = friday_end = saturday_end = sunday_end = None


    schedule = Schedule.objects.get_or_create(monday_start=monday_start,\
                                            monday_end=monday_end,\
                                            tuesday_start=tuesday_start,\
                                            tuesday_end=tuesday_end,\
                                            wednesday_start=wednesday_start,\
                                            wednesday_end=wednesday_end,\
                                            thursday_start=thursday_start,\
                                            thursday_end=thursday_end,\
                                            friday_start=friday_start,\
                                            friday_end=friday_end,\
                                            saturday_start=saturday_start,
                                            saturday_end=saturday_end,\
                                            sunday_start=sunday_start,\
                                            sunday_end=sunday_end)[0]
    schedule.save()
    return schedule

def populate_single_Schedule():

    monday_start = tuesday_start = wednesday_start = None
    thursday_start = friday_start = saturday_start = sunday_start = None

    monday_end = tuesday_end = wednesday_end = None
    thursday_end = friday_end = saturday_end = sunday_end = None

    if random.randint(1, 1000) % 2:
        monday_start = str(random.randint(11, 14)) + ':00'
        monday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        tuesday_start = str(random.randint(11, 14)) + ':00'
        tuesday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        wednesday_start = str(random.randint(11, 14)) + ':00'
        wednesday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        thursday_start = str(random.randint(11, 14)) + ':00'
        thursday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        friday_start = str(random.randint(11, 14)) + ':00'
        friday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        saturday_start = str(random.randint(11, 14)) + ':00'
        saturday_end = str(random.randint(14, 16)) + ':00'

    if random.randint(1, 1000) % 2:
        sunday_start = str(random.randint(11, 14)) + ':00'
        sunday_end = str(random.randint(14, 16)) + ':00'


    schedule = Schedule.objects.get_or_create(monday_start=monday_start,\
                                            monday_end=monday_end,\
                                            tuesday_start=tuesday_start,\
                                            tuesday_end=tuesday_end,\
                                            wednesday_start=wednesday_start,\
                                            wednesday_end=wednesday_end,\
                                            thursday_start=thursday_start,\
                                            thursday_end=thursday_end,\
                                            friday_start=friday_start,\
                                            friday_end=friday_end,\
                                            saturday_start=saturday_start,
                                            saturday_end=saturday_end,\
                                            sunday_start=sunday_start,\
                                            sunday_end=sunday_end)[0]
    schedule.save()
    return schedule

def populate_BasicUser(N=10):
    for entry in range(N):
        email = fakegen.email()
        last_name = fakegen.last_name()
        first_name = fakegen.first_name()
        phone_number = random.randint(3000000, 9000000)

        type = random.choice(['PR', 'RE'])

        hashed_password = '123456789'

        #add restaurant, program, courier
        basic_user = UserClass.objects.create_basic_user(email=email, last_name=last_name,\
                            first_name=first_name,\
                            phone_number=phone_number,\
                            type=type, password=hashed_password)

        if entry % 2:
            if type == 'PR':
                basic_user.user_object.program = populate_single_program(basic_user)

            elif type == 'RE':
                basic_user.user_object.restaurant = populate_single_restaurant(basic_user)

            basic_user.user_object.save()

            # Create requests
            if entry % 5:
                created_at = fakegen.date_time_this_year()
                user_id = basic_user
                schedule_id = None
                request_change = None
                request_type = random.choice(['PR', 'SC', 'PA', 'O'])

                if request_type == 'SC':
                    schedule_id = populate_single_Schedule()
                else:
                    request_change = fakegen.sentence()

                current_request_review_id = None

                request = Request.objects.get_or_create(created_at=created_at,\
                                                        user_id=basic_user, schedule_id=schedule_id,\
                                                        request_change=request_change,
                                                        current_request_review_id=current_request_review_id,\
                                                        request_type=request_type)[0]

                request_review = RequestReview.objects.get_or_create(created_at=created_at,\
                                                        request_id=request,\
                                                        status='P')[0]

                if random.randint(1, 1000) % 2:
                    # Approve
                    request.current_request_review_id = request_review
                    request_review.status='A'
                else:
                    if random.randint(1, 1000) % 2:
                        #Reject
                        request_review.status='R'
                    request.current_request_review_id = request_review

                request_review.save()
                request.save()

                notification = Notification.objects.get_or_create(created_at=created_at, notification_type='R', is_dismissed=False,\
                                                request=request)[0]
                notification.save()

                notification = Notification.objects.get_or_create(created_at=created_at, notification_type='C',
                                                                is_dismissed=False, basic_user=basic_user)[0]
                notification.save()

def populate_AdminUser(N=10):
    for entry in range(N):
        # active = bool(random.getrandbits(1))
        email = fakegen.email()
        last_name = fakegen.last_name()
        first_name = fakegen.first_name()
        phone_number = random.randint(3000000, 9000000)
        role = random.choice(['ADMIN', 'SUPER', 'MNGR', 'DEV', 'STAFF'])
        hashed_password = '123456789'

        if role == 'SUPER':
            admin_user = UserClass.objects.create_superuser(email=email,\
                                                    last_name=last_name,\
                                                    first_name=first_name,\
                                                    phone_number=phone_number,\
                                                    password=hashed_password)
        else:
            admin_user = UserClass.objects.create_staffuser(email=email,\
                                                    last_name=last_name,\
                                                    first_name=first_name,\
                                                    phone_number=phone_number, role=role,\
                                                    password=hashed_password)
        admin_user.save()

def populate_single_restaurant (BasicUser):
    created_at = fakegen.date_time_this_year()
    company_name = fakegen.company()
    main_contact = BasicUser
    phone_number = random.randint(3000000, 9000000)
    schedule = populate_single_restaurant_Schedule()
    role = random.choice(['ADMIN', 'SUPER', 'MNGR', 'DEV', 'STAFF'])
    meals = random.randint(1, 10000)
    uber_eats = bool(random.getrandbits(1))
    delivery_capacity = bool(random.getrandbits(1))
    packaging = bool(random.getrandbits(1))
    health_certificate = fakegen.address()
    address = fakegen.address()
    coordinates = fakegen.name()
    latitude = 43.656560
    longitude = -79.435408

    # create application review
    app_review = ApplicationReview.objects.create(created_at=created_at,\
                                                    type=BasicUser.user_object.type,
                                                    model_id=BasicUser,
                                                    status='P')

    if random.randint(1, 1000) % 2:
        # Approve
        review = None
        app_review.status = 'A'
        app_review.admin_by_id = random.choice(UserClass.objects.filter(user_type='ADM'))
        app_review.save()
    else:
        if random.randint(1, 1000) % 2:
            # Reject
            app_review.status = 'R'
            app_review.comments = fakegen.sentence()
            app_review.admin_by_id = random.choice(UserClass.objects.filter(user_type='ADM'))
            app_review.save()
        review = app_review

    # adding a notification for the application review
    notification = \
    Notification.objects.get_or_create(created_at=created_at, notification_type='A', is_dismissed=False,
                                    application=app_review)[0]
    notification.save()

    restaurant = Restaurant.objects.get_or_create(created_at=created_at,\
                                                company_name=company_name,\
                                                main_contact=main_contact,\
                                                phone_number=phone_number,\
                                                schedule=schedule,\
                                                meals=meals,\
                                                uber_eats=uber_eats,\
                                                delivery_capacity=delivery_capacity,\
                                                packaging=packaging,\
                                                health_certificate=health_certificate,\
                                                address=address,\
                                                coordinates=coordinates,\
                                                latitude=latitude,\
                                                longitude=longitude,\
                                                review=review)[0]
    restaurant.save()
    return restaurant

def populate_single_program (BasicUser):
    created_at = fakegen.date_time_this_year()
    program_name = fakegen.company()
    main_contact = BasicUser
    phone_number = random.randint(3000000, 9000000)
    schedule = populate_single_Schedule()
    address = fakegen.address()
    meals = random.randint(1, 10000)
    coordinates = fakegen.name()
    latitude = 43.658726
    longitude = -79.418821

    # create application review
    app_review = ApplicationReview.objects.create(created_at=created_at,\
                                                    type=BasicUser.user_object.type,\
                                                    model_id=BasicUser,\
                                                    status='P')

    if random.randint(1, 1000) % 2:
        # Approve
        review = None
        app_review.status = 'A'
        app_review.admin_by_id = random.choice(UserClass.objects.filter(user_type='ADM'))
        app_review.save()
    else:
        if random.randint(1, 1000) % 2:
            # Reject
            app_review.status = 'R'
            app_review.comments = fakegen.sentence()
            app_review.admin_by_id = random.choice(UserClass.objects.filter(user_type='ADM'))
            app_review.save()
        review = app_review

    # added a notification for application review
    notification = Notification.objects.get_or_create(created_at=created_at, notification_type='A', is_dismissed=False, application=app_review)[0]
    notification.save()

    program = Program.objects.get_or_create(created_at=created_at, program_name=program_name,\
                                            main_contact=main_contact,\
                                            phone_number=phone_number,\
                                            schedule=schedule,\
                                            meals=meals,\
                                            address=address,\
                                            coordinates=coordinates,\
                                            latitude=latitude,\
                                            longitude=longitude,\
                                            review=review)[0]

    program.save()
    return program

def populate_Restaurant(N=10):
    for entry in range(N):
        created_at = fakegen.date_time_this_year()
        company_name = fakegen.name()
        main_contact = random.choice(BasicUser.objects.all())
        phone_number = random.randint(3000000, 9000000)
        schedule = random.choice(Schedule.objects.all())
        meals = random.randint(1, 10000)
        uber_eats = bool(random.getrandbits(1))
        delivery_capacity = bool(random.getrandbits(1))
        packaging = bool(random.getrandbits(1))
        health_certificate = fakegen.address()
        address = fakegen.address()
        coordinates = fakegen.name()
        review = None

        restaurant = Restaurant.objects.get_or_create(created_at=created_at,\
                                                    company_name=company_name,\
                                                    main_contact=main_contact,\
                                                    phone_number=phone_number,\
                                                    schedule=schedule,\
                                                    meals=meals,\
                                                    uber_eats=uber_eats,\
                                                    delivery_capacity=delivery_capacity,\
                                                    packaging=packaging,\
                                                    health_certificate=health_certificate,\
                                                    address=address,\
                                                    coordinates=coordinates,\
                                                    review=review)[0]
        restaurant.save()

def populate_Program(N=30):
    for entry in range(N):
        created_at = fakegen.date_time_this_year()
        program_name = fakegen.name()
        main_contact = random.choice(BasicUser.objects.all())
        phone_number = random.randint(3000000, 9000000)
        schedule = random.choice(Schedule.objects.all())
        address = fakegen.address()
        coordinates = fakegen.name()
        review = None

        program = Program.objects.get_or_create(created_at=created_at, program_name=program_name,\
                                                main_contact=main_contact,\
                                                phone_number=phone_number,\
                                                schedule=schedule,\
                                                address=address,\
                                                coordinates=coordinates,\
                                                review=review)[0]

        program.save()

def populate_Request(N=10):
    for entity in range(N):
        created_at = fakegen.date_time_this_year()
        user_id = random.choice(BasicUser.objects.all())
        schedule_id = random.choice(Schedule.objects.all())

        request_change = fakegen.address()
        current_request_review_id = None

        request_type = random.choice(['PR', 'SC', 'PA'])

        request = Request.objects.get_or_create(created_at=created_at,\
                                                user_id=user_id, schedule_id=schedule_id,\
                                                request_change=request_change,
                                                current_request_review_id=current_request_review_id,\
                                                request_type=request_type)[0]

        request.save()

        notification = Notification.objects.get_or_create(created_at=created_at, notification_type='R', is_dismissed=False, request=request)[0]
        notification.save()

def populate_Pairing(N=10):
    for entity in range(N):

        restaurant_id = random.choice(Restaurant.objects.all())
        program_id = random.choice(Program.objects.all())

        restaurant_id.schedule = program_id.schedule

        restaurant_id.save()

        meals = random.randint(10, 60)

        try:
            pairing = Pairings.objects.get(program_id=program_id, restaurant_id=restaurant_id)
            pairing.schedule_id = restaurant_id.schedule
            pairing.meals = meals
            pairing.save()

        except Pairings.DoesNotExist:
            pairing = Pairings.objects.get_or_create(restaurant_id=restaurant_id,\
                                                    program_id=program_id, schedule_id=restaurant_id.schedule, meals=meals)[0]

def populate_ApplicationReview(N=30):
    for entry in range(N):
        created_at = fakegen.date_time_this_year()
        status = random.choice(['P', 'R', 'A'])
        admin_by_id = random.choice(AdminUser.objects.all())
        model_id = random.choice(BasicUser.objects.all())
        type = random.choice(['PR', 'RE'])
        applicationReview = ApplicationReview.objects.get_or_create(created_at = created_at, status = status,
                                                            admin_by_id = admin_by_id, model_id = model_id, type = type)[0]

        applicationReview.save()

        notification = Notification.objects.get_or_create(created_at=created_at, notification_type='A', is_dismissed=False, application=applicationReview)[0]
        notification.save()

if __name__ == '__main__':

    populate_AdminUser(40)
    # This creates Restaurants and Programs at random (simulates application)
    # Creates schedule as well (as part of restaurant/program creation)
    # Also creates applications (as part of restaurant/program creation) <-- ALL IN PENDING STATUS
    populate_BasicUser(40)
    # BasicUser creates random requests for end users
    populate_Pairing(10)

    # Create initial meal meal_count
    MealHistory.objects.create(meals=random.randint(100, 2000))
