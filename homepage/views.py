"""views"""
from django.shortcuts import render, redirect
import datetime
from profiles.models import Restaurant, Schedule, Program
from applications.models import Pairings, Notification
from applications.models import ApplicationReview
from documents.models import Document
from django.contrib.auth.decorators import login_required
from homepage import email_vendor
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Q
import mimetypes
from django.http import StreamingHttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
ICON_DIR = os.path.join(IMAGES_DIR, 'icon')
PROFILE_IMG_DIR = os.path.join(ICON_DIR, 'profile_image')



def __get_model(user):
    # get model of restaurant or program
    type_dict = {'RE': 'restaurant', 'PR': 'program'}
    model = getattr(user.user_object, type_dict[user.user_object.type])
    return model


@login_required(login_url='/login')
def apply(request):
    user = request.user

    if user.user_type == 'ADM':
        return redirect('/admin/applications')

    model = __get_model(user)

    # Check if already applied and approved
    if model and not model.review:
        return redirect('/')

    if request.method == 'POST':

        position = request.POST.get('position')
        phone_number = request.POST.get('phone_number')
        meals = request.POST.get('meals')
        address = request.POST.get('address')

        created_at = datetime.datetime.now()
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')

        # Create schedule model
        monday_start = tuesday_start = wednesday_start = None
        thursday_start = friday_start = saturday_start = sunday_start = None

        if user.user_object.type == 'RE':
            schedule_available = request.POST.get('schedule_available')

            if schedule_available == 'True':
                monday_start = '15:00'
                tuesday_start = '15:00'
                wednesday_start = '15:00'
                thursday_start = '15:00'
                friday_start = '15:00'
        else:
            schedule = request.POST.getlist('schedule')
            start_time = request.POST.get('start_time')
            for day in schedule:
                if day =='MO':
                    monday_start = start_time
                elif day =='TU':
                    tuesday_start = start_time
                elif day =='WE':
                    wednesday_start = start_time
                elif day =='TH':
                    thursday_start = start_time
                elif day =='FR':
                    friday_start = start_time
                elif day =='SA':
                    saturday_start = start_time
                elif day =='SU':
                    sunday_start = start_time

        schedule_model = Schedule.objects.get_or_create(monday_start=monday_start,\
                                            tuesday_start=tuesday_start,\
                                            wednesday_start=wednesday_start,\
                                            thursday_start=thursday_start,\
                                            friday_start=friday_start,\
                                            saturday_start=saturday_start,\
                                            sunday_start=sunday_start)[0]
        schedule_model.save()

        # create application review
        app_review = ApplicationReview.objects.create(created_at=created_at,\
                                                        type=user.user_object.type,
                                                        model_id=user,
                                                        status='P')
        app_review.save()

        # create new notification
        notification = Notification.objects.get_or_create(notification_type='A', is_dismissed=False, \
                                        application=app_review)[0]
        notification.save()

        # send emails
        email_vendor.email_admin_new_application(app_review)
        email_vendor.email_user_new_application(app_review)

        if user.user_object.type == 'RE':
            name = request.POST.get('company_name')
            uber_eats = request.POST.get('uber_eats')
            health_certificate = request.POST.get('health_certificate')

            if not model:
                # Create Restaurant model
                restaurant = Restaurant.objects.get_or_create(created_at=created_at,\
                                                    company_name=name,\
                                                    main_contact=user,\
                                                    phone_number=phone_number,\
                                                    schedule=schedule_model,\
                                                    meals=meals,\
                                                    uber_eats=uber_eats,\
                                                    health_certificate=health_certificate,\
                                                    address=address,\
                                                            longitude=longitude, \
                                                            latitude = latitude, \
                                                    review=app_review)[0]
            else:
                restaurant = model
                restaurant.company_name = name
                restaurant.phone_number = phone_number
                restaurant.schedule = schedule_model
                restaurant.meals = meals
                restaurant.uber_eats = uber_eats
                restaurant.health_certificate = health_certificate
                restaurant.address = address
                restaurant.review = app_review
                # restaurant.coordinates = coordinates
                restaurant.longitude = longitude
                restaurant.latitude = latitude

            restaurant.save()
            user.user_object.restaurant = restaurant
        else:
            name = request.POST.get('program_name')

            if not model:
                # Create Program model
                program = Program.objects.get_or_create(created_at=created_at,\
                                                    program_name=name,\
                                                    main_contact=user,\
                                                    phone_number=phone_number,\
                                                    schedule=schedule_model,\
                                                    meals=meals,\
                                                    address=address,\
                                                    # coordinates=coordinates,\
                                                        longitude=longitude,\
                                                        latitude=latitude,\
                                                    review=app_review)[0]
            else:
                program = model
                program.program_name = name
                program.phone_number = phone_number
                program.schedule = schedule_model
                program.meals = meals
                program.address = address
                program.review = app_review
                program.coordinates = coordinates
                program.longitude = longitude
                program.latitude = latitude

            program.save()
            user.user_object.program = program

        user.user_object.position = position
        user.user_object.save()

        user.phone_number = phone_number
        user.save()
        return redirect('/application/status')
    else:
        # GET Request

        # Check if already applied
        if model and model.review:
            return redirect('/application/status')

        return render(request, 'applications/apply.html', {'user': user})

@login_required(login_url='/login')
def apply_status(request):
    user = request.user

    if user.user_type == 'ADM':
        return redirect('/admin/applications')

    # Redirect to admin homepage is admin user signed in
    if user.user_type == 'ADM':
        return redirect('/admin/')

    model = __get_model(user)

    # Check if approved
    if not model.review:
        return redirect('/')

    return render(request, 'applications/application_status.html', {'user': user,\
        'schedule': model.schedule, 'review': model.review})


@login_required(login_url='/login')
def homepage(request):
    current_user = request.user

    # Redirect to admin homepage is admin user signed in
    if current_user.user_type == 'ADM':
        return redirect('/admin/')

    model = __get_model(current_user)

    # Has not applied
    if not model:
        return redirect('/apply/')
    elif model.review:
        # Application not approved
        return redirect('/application/status/')

    # Get partner (paired) information
    pairing_info = []

    schedule = model.schedule.getSchedule()
    schedule['monday_start_meals'] = 0
    schedule['tuesday_start_meals'] = 0
    schedule['wednesday_start_meals'] = 0
    schedule['thursday_start_meals'] = 0
    schedule['friday_start_meals'] = 0

    if current_user.user_object.type == 'PR':
        all_pairings = Pairings.objects.filter(program_id=current_user.user_object.program)
        for pairing in all_pairings:

            if not schedule['monday_start']:
                schedule['monday_start'] = pairing.restaurant_id.schedule.monday_start
            if pairing.restaurant_id.schedule.monday_start:
                schedule['monday_start_meals'] += pairing.meals

            if not schedule['tuesday_start']:
                schedule['tuesday_start'] = pairing.restaurant_id.schedule.tuesday_start
            if pairing.restaurant_id.schedule.tuesday_start:
                schedule['tuesday_start_meals'] += pairing.meals

            if not schedule['wednesday_start']:
                schedule['wednesday_start'] = pairing.restaurant_id.schedule.wednesday_start
            if pairing.restaurant_id.schedule.wednesday_start:
                schedule['wednesday_start_meals'] += pairing.meals

            if not schedule['thursday_start']:
                schedule['thursday_start'] = pairing.restaurant_id.schedule.thursday_start
            if pairing.restaurant_id.schedule.thursday_start:
                schedule['thursday_start_meals'] += pairing.meals

            if not schedule['friday_start']:
                schedule['friday_start'] = pairing.restaurant_id.schedule.friday_start
            if pairing.restaurant_id.schedule.friday_start:
                schedule['friday_start_meals'] += pairing.meals

            pairing.restaurant_id.meals = pairing.meals
            pairing_info.append(pairing.restaurant_id)

    elif current_user.user_object.type == 'RE':
        all_pairings = Pairings.objects.filter(restaurant_id=current_user.user_object.restaurant)
        for pairing in all_pairings:

            if not schedule['monday_start']:
                schedule['monday_start'] = pairing.program_id.schedule.monday_start
            if pairing.program_id.schedule.monday_start:
                schedule['monday_start_meals'] += pairing.meals

            if not schedule['tuesday_start']:
                schedule['tuesday_start'] = pairing.program_id.schedule.tuesday_start
            if pairing.program_id.schedule.tuesday_start:
                schedule['tuesday_start_meals'] += pairing.meals

            if not schedule['wednesday_start']:
                schedule['wednesday_start'] = pairing.program_id.schedule.wednesday_start
            if pairing.program_id.schedule.wednesday_start:
                schedule['wednesday_start_meals'] += pairing.meals

            if not schedule['thursday_start']:
                schedule['thursday_start'] = pairing.program_id.schedule.thursday_start
            if pairing.program_id.schedule.thursday_start:
                schedule['thursday_start_meals'] += pairing.meals

            if not schedule['friday_start']:
                schedule['friday_start'] = pairing.program_id.schedule.friday_start
            if pairing.program_id.schedule.friday_start:
                schedule['friday_start_meals'] += pairing.meals

            pairing.program_id.meals = pairing.meals
            pairing_info.append(pairing.program_id)

    return render(request, 'homepage/endUser-homepage.html', {'user': current_user,
        'schedule': schedule, 'pairing_info': pairing_info})


@login_required(login_url='/login')
def user_settings (request):
    current_user = request.user
    if request.method == 'POST' and request.FILES['profile_image']:
        big_dict = {}
        myfile = request.FILES['profile_image']
        fs = FileSystemStorage()
        fs.location = PROFILE_IMG_DIR
        filename = fs.save(myfile.name, myfile)
        current_user.image = filename
        current_user.save()

        big_dict["user"] = current_user
        big_dict["image_path"] = os.path.join('images/icon/profile_image/', filename)

        return render (request,'profiles/settings.html', context=big_dict )
    else:
        big_dict = {}
        big_dict["image_path"] = os.path.join('images/icon/profile_image/', current_user.image)
        big_dict["user"] = current_user
        return render (request,'profiles/settings.html', context=big_dict )



def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

@login_required(login_url='/login')
def user_resources (request):
    current_user = request.user
    try:
        request.POST.get('download')

    except Exception:
        pass

    if request.method == 'POST' and request.POST.get('download'):
        file_name = request.POST.get('download')

        RESOURCES_DIR = os.path.join(STATIC_DIR, 'resources')
        FILE_PATH = os.path.join(RESOURCES_DIR, file_name)
        if os.path.exists(FILE_PATH):
            result = mimetypes.guess_type(FILE_PATH)
            if result:
                content_type = result[0]
            else:
                print("MIME type cannot be detected")

            response = StreamingHttpResponse(readFile(FILE_PATH))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
            return response
    else:
        if current_user.user_object.type == 'PR':
            big_dict = {}
            big_dict["user"] = current_user

            lst = []
            satisfied_doc = Document.objects.filter(Q(owner_type='PR') | Q(owner_type='BOTH'))
            for doc in satisfied_doc:
                path = '/static/resources/' + str(doc.name)
                print(path)
                lst.append([doc.name, doc.size, path])
            big_dict["resources"] = lst
            return render (request,'profiles/resources.html', context=big_dict)

        elif current_user.user_object.type == 'RE':
            big_dict = {}
            big_dict["user"] = current_user 

            lst = []
            satisfied_doc = Document.objects.filter(Q(owner_type='RE') |Q(owner_type='BOTH'))
            for doc in satisfied_doc:
                path = '/static/resources/' + str(doc.name)
                print(path)
                lst.append([doc.name, doc.size])
            big_dict["resources"] = lst
            return render (request,'profiles/resources.html', context=big_dict)
