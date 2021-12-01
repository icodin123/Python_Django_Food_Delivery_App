from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from applications.models import Request, ApplicationReview, MealHistory
from applications.models import Pairings, PairingsManager
from profiles.models import Restaurant, Program, Schedule, BasicUser
from documents.models import Document
from applications.models import RequestReview, Notification
from documents.models import NoteManager, DocumentManager
from braces.views import SelectRelatedMixin
from profiles.models import UserClass
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
import os
from django.core.files.storage import FileSystemStorage
from homepage.settings import GOOGLE_API_KEY
from homepage import email_vendor
from django.db.models import Sum

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'static')
IMAGES_DIR = os.path.join(TEMPLATE_DIR, 'images')
RESOURCE_DIR = os.path.join(TEMPLATE_DIR, 'resources')
ICON_DIR = os.path.join(IMAGES_DIR, 'icon')
PROFILE_IMG_DIR = os.path.join(ICON_DIR, 'profile_image')
SIZE_UNIT_LIST = ['B', 'KB', 'MB', 'GB']


def get_today_schedule_entries(weekday, all_pairing):
    """Return schedule entries that correspond to the given weekday and all pairings"""
    satisfying_pairing = []

    for pair in all_pairing:
        schedule_object = pair.schedule_id
        whole_week_delivery = [schedule_object.monday_start, schedule_object.tuesday_start,
                            schedule_object.wednesday_start,
                            schedule_object.thursday_start, schedule_object.friday_start,
                            schedule_object.saturday_start,
                            schedule_object.sunday_start]

        if whole_week_delivery[weekday] is not None:
            if weekday == 0:
                time_string = schedule_object.monday_start.strftime("%-I:%M %p")
            if weekday == 1:
                time_string = schedule_object.tuesday_start.strftime("%-I:%M %p")
            if weekday == 2:
                time_string = schedule_object.wednesday_start.strftime("%-I:%M %p")
            if weekday == 3:
                time_string = schedule_object.thursday_start.strftime("%-I:%M %p")
            if weekday == 4:
                time_string = schedule_object.friday_start.strftime("%-I:%M %p")
            if weekday == 5:
                time_string = schedule_object.saturday_start.strftime("%-I:%M %p")
            if weekday == 6:
                time_string = schedule_object.sunday_start.strftime("%-I:%M %p")

            satisfying_pairing.append((pair.restaurant_id.company_name, pair.program_id.program_name,
                                    time_string, pair.restaurant_id.main_contact.first_name,
                                    pair.restaurant_id.main_contact.last_name, pair.meals,
                                    pair.restaurant_id.id, pair.program_id.id, pair.restaurant_id, pair.program_id))
    return satisfying_pairing


@login_required(login_url='/admin/login')
def admin_homepage(request):
    """Return response that corresponds to the admin homepage"""
    current_user = request.user

    if current_user.user_type == 'ADM':
        current_user_id = current_user.id
        weekday = datetime.datetime.now().weekday()
        all_pairing = Pairings.objects.all()
        big_dict = {}

        satisfying_pairing = get_today_schedule_entries(weekday, all_pairing)
        big_dict["daily_schedule"] = satisfying_pairing

        # Dashboard stats
        big_dict["restaurant_count"] = Restaurant.objects.all().count()
        big_dict["program_count"] = Program.objects.all().count()
        big_dict["application_count"] = ApplicationReview.objects.filter(status="P").count()

        today = datetime.datetime.today()
        big_dict['todays_date'] = today.strftime('%b %-d')

        # Get lifetime meals
        start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0) # represents 00:00:00
        end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59) # represents 23:59:59
        todays_count = MealHistory.objects.filter(created_at__range=(start_date, end_date))

        # Check if new pairs need to be added for today
        for pair in satisfying_pairing:
            to_be_added = True
            for pair_counted in todays_count:
                if pair_counted.restaurant_id and pair_counted.program_id and pair[6] == pair_counted.restaurant_id.id and pair[7] == pair_counted.program_id.id:
                        to_be_added = False
            if to_be_added:
                MealHistory.objects.create(restaurant_id=pair[8], program_id=pair[9], meals=pair[5])

        big_dict["meal_count"] = MealHistory.objects.aggregate(Sum('meals'))['meals__sum']
        if not big_dict["meal_count"]:
            big_dict["meal_count"] = 0

        return render(request, 'homepage/admin-homepage.html', context=big_dict)

    elif current_user.user_type == 'BSC':
        return redirect('/')


@login_required(login_url='/admin/login')
def meal_history(request):

    if request.user.user_type == 'BSC':
        return redirect("/")

    meals_paired = MealHistory.objects.all()

    return render(request, 'admin/meal-history.html', context={"meals_paired": meals_paired})


@login_required(login_url='/admin/login')
def meal_history_update(request):

    if request.user.user_type == 'BSC':
        return redirect("/")

    if request.method == "POST":
        history_id = request.POST.get('history_id')
        meal_history = MealHistory.objects.get(id=history_id)

        if meal_history:
            meal_history.meals = request.POST.get('meals_count')

        meal_history.save()


    return redirect("/admin/mealhistory")


def admin_login(request):
    """Login user based on provided credentials"""
    # if request type is POST
    if request.method == 'POST':
        # get credentials
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        # check if user was retrieved from the database
        if user:
            # if user is active
            if user.is_active:
                # do login
                login(request, user)
                # return response for index page
                return redirect('/')
            else:
                # return response that account is inactive
                return HttpResponse("Account is inactive")
        else:
            print("login failed")
            return redirect("/admin/login")
    else:
        # redirect user to login page
        return render(request, 'profiles/admin_login.html', {})


@login_required(login_url='/admin/login')
def view_user_profile(request, id):
    """Return response that corresponds to profile of the user with given id"""
    if request.user.user_type == 'BSC':
        return redirect('/')

    try:
        view_user = UserClass.objects.get(id=id)
    except UserClass.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # If viewing themselves, direct to settings
    if request.user.id == view_user.id:
        return redirect("/admin/settings")

    return render(request, "profiles/profile.html", {'view_user': view_user})


@login_required(login_url='/admin/login')
def edit_user_profile(request, id):
    """Edit profile of the user with given id."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    if request.method == "POST":
        try:
            view_user = UserClass.objects.get(id=id)
        except UserClass.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        view_user.email = request.POST.get('email')
        view_user.first_name = request.POST.get('first_name')
        view_user.last_name = request.POST.get('last_name')
        view_user.phone_number = request.POST.get('phone_number')
        view_user.active = request.POST.get('is_active')

        try:
            view_user.save()
        except IntegrityError:
            pass

        return redirect('/admin/user/' + str(view_user.id))

    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/admin/login')
def admin_settings(request):
    """Implements handling of post and get requests for the admin settings page"""
    current_user = request.user

    big_dict = {}

    if current_user.user_type == "ADM":
        admin_list = UserClass.objects.filter(user_type = 'ADM')
        big_dict["admins"] = admin_list

    if request.user.user_type == 'BSC':
        return redirect('/')

    if request.method == 'POST' and request.FILES['profile_image']:
        myfile = request.FILES['profile_image']
        fs = FileSystemStorage()
        fs.location = PROFILE_IMG_DIR
        filename = fs.save(myfile.name, myfile)
        current_user.image = filename
        current_user.save()

        big_dict["user"] = current_user
        big_dict["image_path"] = os.path.join('images/icon/profile_image/', filename)

        return render(request, 'profiles/admin_settings.html', context=big_dict)
    else:
        big_dict["image_path"] = os.path.join('images/icon/profile_image/', current_user.image)
        big_dict["user"] = current_user
        return render(request, 'profiles/admin_settings.html', context=big_dict)


@login_required(login_url='/login')
def settings_update_name(request, id):
    """Update name in settings"""
    if request.method == "POST":
        new_first_name = request.POST.get("newFirstName")
        new_last_name = request.POST.get("newLastName")
        request.user.first_name = new_first_name
        request.user.last_name = new_last_name
        request.user.save()
    if request.user.user_type == 'ADM':
        return redirect('/admin/settings')
    return redirect('/settings')


@login_required(login_url='/login')
def settings_update_email (request, id):
    """Update email in settings"""
    if request.method == "POST":
        new_email = request.POST.get("newEmail")
        request.user.email = new_email
        request.user.save()

    if request.user.user_type == 'ADM':
        return redirect('/admin/settings')
    return redirect('/settings')


@login_required(login_url='/login')
def settings_update_password (request, id):
    """Update password in settings"""
    if request.method == "POST":
        old_password = request.POST.get("currentPass")
        current_password = request.user.password

        matchcheck = check_password(old_password, current_password)

        if matchcheck:
            new_password = request.POST.get("newPass")
            confirm_new_password = request.POST.get("confirmNewPass")
            request.user.set_password(new_password)
            update_session_auth_hash(request, request.user)
            request.user.save()
        if request.user.user_type == 'ADM':
            return redirect('/admin/settings')
        return redirect('/settings')


@login_required(login_url='/login')
def settings_add_admins(request, id):
    """Implements feature that allows to add more admins in settings"""
    if request.method == "POST":
        email = request.POST.get("new_admin_email")
        last_name = request.POST.get("new_admin_last_name")
        first_name = request.POST.get("new_admin_first_name")
        phone_number = request.POST.get("new_admin_phone")
        role = request.POST.get("admin_role")
        hashed_password = '123456789'

        if role == 'SUPER':
            admin_user = UserClass.objects.create_superuser(email=email,
                                                            last_name=last_name,
                                                            first_name=first_name,
                                                            phone_number=phone_number,
                                                            password=hashed_password)
        else:
            admin_user = UserClass.objects.create_staffuser(email=email,
                                                            last_name=last_name,
                                                            first_name=first_name,
                                                            phone_number=phone_number, role=role,
                                                            password=hashed_password)
        admin_user.save()

        if request.user.user_type == 'ADM':
            return redirect('/admin/settings')
        return redirect('/settings')


@login_required(login_url='/admin/login')
def applications(request):
    """Implements view that displays applications received by admins"""
    if request.user.user_type == 'BSC':
        return redirect('/')

    application_review_list_programs = ApplicationReview.objects.filter(type='PR').filter(status='P')
    application_review_list_restaurants = ApplicationReview.objects.filter(type='RE').filter(status='P')
    review_application_dict = {'program_app': application_review_list_programs,
                            'restaurant_app': application_review_list_restaurants}

    return render(request, 'admin/applications.html', context=review_application_dict)


@login_required(login_url='/admin/login')
def requests(request):
    """Implements view that displays requests received by admins"""
    if request.user.user_type == 'BSC':
        return redirect('/')

    request_reviews = RequestReview.objects.all().filter(status='P')

    return render(request, 'admin/requests.html', context={'request_reviews': request_reviews})


@login_required(login_url='/admin/login')
def programs(request):
    """Implements view that displays list of programs in the admin portal."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    programs = Program.objects.order_by('program_name')
    approved_programs = []
    for program in programs:
        if not program.review:
            approved_programs.append(program)

    if request.method == "POST":
        email = request.POST.get("contact_email")
        last_name = request.POST.get("contact_last_name")
        first_name = request.POST.get("contact_first_name")
        phone_number = request.POST.get("contact_phone")
        type = 'PR'
        hashed_password = '123456789'

        if (UserClass.objects.filter(email = email)):
            basic_user = UserClass.objects.filter(email = email)[0]
        else:
            basic_user = UserClass.objects.create_basic_user(email=email, last_name=last_name,\
                                first_name=first_name,\
                                phone_number=phone_number,\
                                type=type, password=hashed_password)

        created_at = datetime.datetime.now()
        program_name = request.POST.get("new_program_name")
        main_contact = basic_user
        phone_number = request.POST.get("new_program_phone")
        schedule = request.POST.getlist('new_program_schedule')
        start_time = request.POST.get('new_rest_start_time')
        meals = request.POST.get("new_program_meals")
        address = request.POST.get("new_program_address")
        coordinates = request.POST.get("new_program_address")
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')

        # Create schedule model
        monday_start = tuesday_start = wednesday_start = None
        thursday_start = friday_start = saturday_start = sunday_start = None

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


        program = Program.objects.get_or_create(created_at=created_at, program_name=program_name,\
                                                main_contact=main_contact,\
                                                phone_number=phone_number,\
                                                schedule=schedule_model,\
                                                meals=meals,\
                                                address=address,\
                                                coordinates=coordinates,\
                                                latitude=latitude,\
                                                longitude=longitude)[0]

        program.save()

        basic_user.user_object.program = program

        basic_user.user_object.save()

    return render(request, 'admin/programs.html', context={'programs': approved_programs})


@login_required(login_url='/admin/login')
def restaurants(request):
    """Implements view that displays list of restaurants in the admin portal."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    restaurants = Restaurant.objects.order_by('company_name')

    approved_restaurants = []
    for restaurant in restaurants:
        if not restaurant.review:
            approved_restaurants.append(restaurant)

    if request.method == "POST":
        email = request.POST.get("contact_email")
        last_name = request.POST.get("contact_last_name")
        first_name = request.POST.get("contact_first_name")
        phone_number = request.POST.get("contact_phone")
        type = 'RE'
        hashed_password = '123456789'

        if (UserClass.objects.filter(email = email)):
            basic_user = UserClass.objects.filter(email = email)[0]
        else:
            basic_user = UserClass.objects.create_basic_user(email=email, last_name=last_name,\
                                first_name=first_name,\
                                phone_number=phone_number,\
                                type=type, password=hashed_password)

        created_at = datetime.datetime.now()
        company_name = request.POST.get("new_rest_name")
        main_contact = basic_user
        phone_number = request.POST.get("new_rest_phone")
        schedule = request.POST.getlist('new_rest_schedule')
        start_time = request.POST.get('new_rest_start_time')
        meals = request.POST.get("new_rest_meals")
        uber_eats = request.POST.get("new_rest_uber")
        health_certificate = request.POST.get("new_rest_health_safety")
        address = request.POST.get("new_rest_address")
        coordinates = request.POST.get("new_rest_address")
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')

        # Create schedule model
        monday_start = tuesday_start = wednesday_start = None
        thursday_start = friday_start = saturday_start = sunday_start = None

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


        restaurant = Restaurant.objects.get_or_create(created_at=created_at,\
                                            company_name=company_name,\
                                            main_contact=main_contact,\
                                            phone_number=phone_number,\
                                            schedule=schedule_model,\
                                            meals=meals,\
                                            uber_eats=uber_eats,\
                                            health_certificate=health_certificate,\
                                            address=address,\
                                                    longitude=longitude, \
                                                    latitude = latitude)[0]

        restaurant.save()

        basic_user.user_object.restaurant = restaurant

        basic_user.user_object.save()

    return render(request, 'admin/restaurants-page.html', context={'restaurants': approved_restaurants})

@login_required(login_url='/admin/login')
def application_review(request, id):
    """Review application from restaurant/partner"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    needed_application = ApplicationReview.objects.get(id=id)
    if needed_application.status == 'P' or needed_application.status == 'R':
        return render(request, 'admin/application-review.html', {"id": id, "application": needed_application})

    return redirect("/admin/applications")


def resources(request):
    """Implements view that displays resources in the admin portal"""
    current_user = request.user
    uploadedDoc = None
    deletedDoc = None
    try:
        uploadedDoc = request.FILES['uploadedDocuments']
    except Exception:
        pass

    try:
        deletedDoc = request.POST.get('deleted_item')
    except Exception:
        pass

    if request.method == 'POST' and uploadedDoc and (
            request.POST.get('program') or request.POST.get('restaurant')):

        uploaded_doc = request.FILES['uploadedDocuments']
        uploaded_doc_name = uploaded_doc.name
        uploaded_doc_raw_size = uploaded_doc.size
        size_unit = 'B'
        size_temp = uploaded_doc_raw_size
        while size_temp // 1024 >= 1:
            size_unit = SIZE_UNIT_LIST[SIZE_UNIT_LIST.index(size_unit) + 1]
            size_temp = size_temp // 1024
        uploaded_doc_size = str(size_temp) + size_unit


        owner_type = None
        if request.POST.get('program'):
            owner_type = request.POST.get('program')
        if request.POST.get('restaurant'):
            owner_type = request.POST.get('restaurant')
        if request.POST.get('program') and request.POST.get('restaurant'):
            owner_type = 'BOTH'

        fs = FileSystemStorage()
        fs.location = RESOURCE_DIR
        # this will not raise error
        fs.delete(uploaded_doc_name)
        fs.save(uploaded_doc_name, uploaded_doc)
        # we must delete from database as well
        Document.objects.filter(name=uploaded_doc_name).delete()

        document_manager = DocumentManager()
        document_manager.create_document(uploaded_doc_name, owner_type, uploaded_doc_size)

        all_docs = Document.objects.all()
        big_dict = {}
        document_lst = []
        for doc in all_docs:
            name = doc.name
            created_at = doc.created_at.strftime("%m/%d/%Y")
            size = doc.size
            document_lst.append([name, size, created_at])
        big_dict["documents"] = document_lst
        return render (request,'admin/resources.html', context=big_dict)

    elif request.method == 'POST' and deletedDoc:
        item_tobe_deleted = request.POST.get('deleted_item')

        Document.objects.filter(name=item_tobe_deleted).delete()

        all_docs = Document.objects.all()
        big_dict = {}
        document_lst = []
        for doc in all_docs:
            name = doc.name
            created_at = doc.created_at.strftime("%m/%d/%Y")
            size = doc.size
            document_lst.append([name, size, created_at])
        big_dict["documents"] = document_lst
        return render (request,'admin/resources.html', context=big_dict)

    else:
        all_docs = Document.objects.all()
        big_dict = {}
        document_lst = []
        for doc in all_docs:
            name = doc.name
            created_at = doc.created_at.strftime("%m/%d/%Y")
            size = doc.size
            document_lst.append([name, size, created_at])
        big_dict["documents"] = document_lst
        return render (request,'admin/resources.html', context=big_dict)



def time_format_converter(time_str):
    """Accepts 12-hour format time string and converts it into 24-hour strings"""

    if time_str[-2:] == "AM" or time_str[-2:] == "PM":
        if time_str[1] == ":":
            time_str = "0" + time_str

        if time_str[0:2] == "12" and time_str[-2:] == "AM":
            return "00:00"
        elif time_str[0:2] == "12" and time_str[-2:] == "PM":
            return "12:00"
        else:
            if time_str[-2:] == "PM":
                return str(int(time_str[0:2]) + 12) + ":00"
            elif time_str[-2:] == "AM":
                return time_str[0:2] + ":00"

    else:

        if time_str[1] == ":":
            time_str = "0" + time_str

        if time_str[0:2] == "12" and time_str[-4:] == "a.m.":
            return "00:00"
        elif time_str[0:2] == "12" and time_str[-4:] == "p.m.":
            return "12:00"
        else:
            if time_str[-4:] == "p.m.":
                return str(int(time_str[0:2]) + 12) + ":00"
            elif time_str[-4:] == "a.m.":
                return time_str[0:2] + ":00"


def string_to_object_time_converter(time_str):
    """Converts 24-hour time string into a datetime object."""
    time_str = time_format_converter(time_str)

    time = datetime.time(int(time_str[0:2]), 00, 00)
    return time


def update_organization_schedule(organization, schedule, start_time):
    """Update organization schedule based on given schedule and start time"""

    seen = {'SU': 0, 'MO': 0, 'TU': 0, 'WE': 0, 'TH': 0, 'FR': 0, 'SA': 0}
    for day in schedule:
        if day == 'MO':
            organization.schedule.monday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'TU':
            organization.schedule.tuesday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'WE':
            organization.schedule.wednesday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'TH':
            organization.schedule.thursday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'FR':
            organization.schedule.friday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'SA':
            organization.schedule.saturday_start = string_to_object_time_converter(start_time)
            seen[day] += 1
        elif day == 'SU':
            organization.schedule.sunday_start = string_to_object_time_converter(start_time)
            seen[day] += 1

    count = 0
    for item in seen.items():
        if item[1] == 0:
            if count == 0:
                organization.schedule.sunday_start = None
            if count == 1:
                organization.schedule.monday_start = None
            if count == 2:
                organization.schedule.tuesday_start = None
            if count == 3:
                organization.schedule.wednesday_start = None
            if count == 4:
                organization.schedule.thursday_start = None
            if count == 5:
                organization.schedule.friday_start = None
            if count == 6:
                organization.schedule.saturday_start = None
        count += 1

        organization.schedule.save()


@login_required(login_url='/admin/login')
def accept(request, id):
    """Accept application from restaurant/partner"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    if request.method == "POST":

        needed_application = ApplicationReview.objects.get(id=id)
        needed_application.admin_by_id = request.user
        needed_application.status = "A"

        if needed_application.model_id.user_object.type == 'RE':

            schedule_available = request.POST.get('schedule_available')

            if schedule_available == 'True':
                needed_application.model_id.user_object.restaurant.schedule.monday_start = '15:00'
                needed_application.model_id.user_object.restaurant.schedule.tuesday_start = '15:00'
                needed_application.model_id.user_object.restaurant.schedule.wednesday_start = '15:00'
                needed_application.model_id.user_object.restaurant.schedule.thursday_start = '15:00'
                needed_application.model_id.user_object.restaurant.schedule.friday_start = '15:00'

            else:
                needed_application.model_id.user_object.restaurant.schedule.monday_start = None
                needed_application.model_id.user_object.restaurant.schedule.tuesday_start = None
                needed_application.model_id.user_object.restaurant.schedule.wednesday_start = None
                needed_application.model_id.user_object.restaurant.schedule.thursday_start = None
                needed_application.model_id.user_object.restaurant.schedule.friday_start = None

            needed_application.model_id.user_object.restaurant.schedule.save()

            restaurant_name_input = request.POST.get("restaurant_name_input", None)
            restaurant_address_input = request.POST.get("address", None)
            restaurant_health_input = request.POST.get("restaurant_health_input", None)
            restaurant_meals_input = request.POST.get("restaurant_meals_input", None)
            delivery_capacity = request.POST.get("delivery_capacity", None)
            uber_eats = request.POST.get("uber_eats", None)
            packaging = request.POST.get("packaging", None)

            needed_application.model_id.user_object.restaurant.latitude = request.POST.get("lat", None)
            needed_application.model_id.user_object.restaurant.longitude = request.POST.get("lng", None)

            if restaurant_name_input:
                needed_application.model_id.user_object.restaurant.company_name = restaurant_name_input

            if restaurant_address_input:
                needed_application.model_id.user_object.restaurant.address = restaurant_address_input

            if restaurant_health_input:
                needed_application.model_id.user_object.restaurant.health_certificate = restaurant_health_input

            if restaurant_meals_input:
                needed_application.model_id.user_object.restaurant.meals = restaurant_meals_input

            if delivery_capacity:
                needed_application.model_id.user_object.restaurant.delivery_capacity = delivery_capacity

            if uber_eats:
                needed_application.model_id.user_object.restaurant.uber_eats = uber_eats

            if packaging:
                needed_application.model_id.user_object.restaurant.packaging = packaging

            needed_application.model_id.user_object.restaurant.review = None
            needed_application.model_id.user_object.restaurant.save()

        elif needed_application.model_id.user_object.type == 'PR':

            program_schedule = request.POST.getlist('program_schedule')
            program_start_time = request.POST.get('program_starttime')

            needed_application.model_id.user_object.program.latitude = request.POST.get("lat", None)
            needed_application.model_id.user_object.program.longitude = request.POST.get("lng", None)

            update_organization_schedule(needed_application.model_id.user_object.program, program_schedule,
                                        program_start_time)

            program_phone_number_input = request.POST.get("program_phone_number_input", None)
            program_name_input = request.POST.get("program_name_input", None)
            program_meals_input = request.POST.get("program_meals_input", None)
            program_address_input = request.POST.get("address", None)

            if program_phone_number_input:
                needed_application.model_id.user_object.program.phone_number = program_phone_number_input

            if program_name_input:
                needed_application.model_id.user_object.program.program_name = program_name_input

            if program_meals_input:
                needed_application.model_id.user_object.program.meals = program_meals_input

            if program_address_input:
                needed_application.model_id.user_object.program.address = program_address_input

            needed_application.model_id.user_object.program.review = None
            needed_application.model_id.user_object.program.save()

        needed_application.save()

    return redirect('/admin/applications')



@login_required(login_url='/admin/login')
def deny(request, id):
    """Deny application from restaurant/partner"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    if request.method == "POST":
        comment = request.POST.get("comment", "")

        needed_application = ApplicationReview.objects.get(id=id)
        needed_application.status = "R"
        needed_application.comments = comment
        needed_application.admin_by_id = request.user
        needed_application.save()

    return redirect('/admin/applications')


@login_required(login_url='/admin/login')
def review_request(request, id):
    """Review request from restaurant/partner"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    needed_request = RequestReview.objects.get(id=id)
    return render(request, 'admin/request-review.html', {"id": id, "request_review": needed_request})


@login_required(login_url='/admin/login')
def accept_request(request, id):
    """Accept request from restaurant/partner."""

    if request.user.user_type == 'BSC':
        return redirect('/')

    needed_request = RequestReview.objects.get(id=id)

    needed_request.status = "A"  # approved
    needed_request.admin_id = request.user
    needed_request.save()

    return redirect('/admin/requests')


@login_required(login_url='/admin/login')
def deny_request(request, id):
    """Deny request from restaurant/partner."""

    if request.user.user_type == 'BSC':
        return redirect('/')

    comment = request.POST.get("comment", "")

    needed_request = ApplicationReview.objects.get(id=id)
    needed_request.status = "R"
    needed_request.comments = comment
    needed_request.admin_id = request.user
    needed_request.save()

    return redirect('/admin/requests')


@login_required(login_url='/admin/login')
def program_profile(request, id):

    if request.user.user_type == 'BSC':
        return redirect('/')

    needed_program = Program.objects.get(id=id)

    # Not approved yet
    if needed_program.review:
        return redirect("/admin/application/" + str(needed_program.review.id) + "/review")

    all_docs = []
    all_notes = []
    result_contacts = []

    all_contacts = BasicUser.objects.filter(program=needed_program)
    for contact in all_contacts:
        result_contacts.append(UserClass.objects.get(user_object=contact))

    try:
        all_notes = needed_program.program_notes.all
    except:
        pass
    return render(request, 'admin/program-profile.html', {"id": id, "program": needed_program, "doc_list": all_docs,
                                                        "notes": all_notes, "contacts": result_contacts})


@login_required(login_url='/admin/login')
def add_program_note(request, id):
    """Add new note to the program"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    note_name = request.POST.get("note_name", "")
    note_content = request.POST.get("note_content", "")

    needed_program = Program.objects.get(id=id)
    note_manager = NoteManager()
    new_note = note_manager.create_note(note_name=note_name, note_content=note_content, owner_type='PR',
                                        program_id=needed_program)
    cur_path = request.path_info
    return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])


@login_required(login_url='/admin/login')
def add_program_contact(request, id):
    """Add new user to the program"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    email = request.POST.get("email", "")
    last_name = request.POST.get("last_name", "")
    first_name = request.POST.get("first_name", "")
    new_user = UserClass.objects.create_basic_user(email=email, password='', last_name=last_name,
                                                first_name=first_name, type='PR')
    needed_program = Program.objects.get(id=id)
    new_user.user_object.program = needed_program
    new_user.user_object.save()
    new_user.save()
    cur_path = request.path_info
    return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])


@login_required(login_url='/admin/login')
def restaurant_profile(request, id):

    if request.user.user_type == 'BSC':
        return redirect('/')

    needed_restaurant = Restaurant.objects.get(id=id)

    # Not approved yet
    if needed_restaurant.review:
        return redirect("/admin/application/" + str(needed_restaurant.review.id) + "/review")

    all_notes = []
    all_docs = []
    result_contacts = []

    all_contacts = BasicUser.objects.filter(restaurant=needed_restaurant)
    for contact in all_contacts:
        result_contacts.append(UserClass.objects.get(user_object=contact))

    try:
        all_notes = needed_restaurant.restaurant_notes.all
    except:
        pass

    return render(request, 'admin/restaurant-profile.html', {"id": id, "restaurant": needed_restaurant,
                                                            "doc_list": all_docs, "notes": all_notes,
                                                            "contacts": result_contacts})


@login_required(login_url='/admin/login')
def add_restaurant_note(request, id):
    """Add new note to the restaurant"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    note_name = request.POST.get("note_name", "")
    note_content = request.POST.get("note_content", "")

    needed_restaurant = Restaurant.objects.get(id=id)
    note_manager = NoteManager()
    new_note = note_manager.create_note(note_name=note_name, note_content=note_content, owner_type='RE',
                                        restaurant_id=needed_restaurant)
    cur_path = request.path_info
    return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])


@login_required(login_url='/admin/login')
def add_restaurant_contact(request, id):
    """Add new user to the restaurant"""

    if request.user.user_type == 'BSC':
        return redirect('/')

    email = request.POST.get("email", "")
    last_name = request.POST.get("last_name", "")
    first_name = request.POST.get("first_name", "")
    new_user = UserClass.objects.create_basic_user(email=email, password='', last_name=last_name,
                                                first_name=first_name, type='RE')
    needed_restaurant = Restaurant.objects.get(id=id)
    new_user.user_object.restaurant = needed_restaurant
    new_user.user_object.save()
    new_user.save()
    cur_path = request.path_info
    return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])


@login_required(login_url='/admin/login')
def pairings(request):

    if request.user.user_type == 'BSC':
        return redirect('/')

    pairings = Pairings.objects.order_by('created_at')
    restaurants = Restaurant.objects.order_by('company_name')
    programs = Program.objects.order_by('program_name')
    return render(request, 'admin/pairings-page.html', context={"pairings": pairings, "programs": programs,
                                                                "restaurants": restaurants,
                                                                "google_api_key": GOOGLE_API_KEY})


@login_required(login_url='/admin/login')
def pairings_add(request):
    """Implements feature that allows admins to create pairings."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    if request.method == "POST":
        program_id = request.POST.get("program_id", "")
        restaurant_id = request.POST.get("restaurant_id", "")

        schedule = request.POST.getlist('schedule')
        start_time = request.POST.get('start_time')

        meals = request.POST.get('meals')

        # Create schedule model
        monday_start = tuesday_start = wednesday_start = None
        thursday_start = friday_start = saturday_start = sunday_start = None

        for day in schedule:
            if day == 'MO':
                monday_start = start_time
            elif day == 'TU':
                tuesday_start = start_time
            elif day == 'WE':
                wednesday_start = start_time
            elif day == 'TH':
                thursday_start = start_time
            elif day == 'FR':
                friday_start = start_time
            elif day == 'SA':
                saturday_start = start_time
            elif day == 'SU':
                sunday_start = start_time

        schedule_model = Schedule.objects.get_or_create(monday_start=monday_start,
                                                        tuesday_start=tuesday_start,
                                                        wednesday_start=wednesday_start,
                                                        thursday_start=thursday_start,
                                                        friday_start=friday_start,
                                                        saturday_start=saturday_start,
                                                        sunday_start=sunday_start)[0]
        schedule_model.save()

        pairings_manager = PairingsManager()

        if program_id != '-1' and program_id != -1 and restaurant_id != '-1' and restaurant_id != -1:
            program_instance = Program.objects.get(id=program_id)
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)

            program_instance.schedule = schedule_model
            restaurant_instance.schedule = schedule_model
            program_instance.save()
            restaurant_instance.save()

            try:
                pairing = Pairings.objects.get(program_id=program_instance, restaurant_id=restaurant_instance)
                pairing.schedule_id = schedule_model
                pairing.meals = meals
                pairing.save()

            except Pairings.DoesNotExist:
                new_pairing = pairings_manager.create_pairing(program_id=program_instance,
                                                            restaurant_id=restaurant_instance,
                                                            schedule_id=schedule_model, meals=meals)

        cur_path = request.path_info
        return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])
    else:
        return redirect("/")


@login_required(login_url='/admin/login')
def pairings_delete(request):
    """Implements feature that allows admins to delete pairings."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    pairing_id = request.POST.get("pairing_id", "")
    pairing = Pairings.objects.get(id=pairing_id)
    pairing.delete()

    cur_path = request.path_info
    return HttpResponseRedirect(cur_path[:cur_path.rfind('/')])


class CreateApplication(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    """This class implements functionality that allows users to create new applications."""
    fields = ("request_type", )
    template = 'applications/request_form.html'


@login_required(login_url='/login')
def requests_list(request):
    """Implements view that allows users to view existing requests"""
    user = request.user

    if user.user_type == 'ADM':
        return redirect('/admin')

    requests = Request.objects.filter(user_id=user)

    return render(request, 'applications/requests.html', {'requests': requests})


@login_required(login_url='/login')
def new_request(request):
    """Implements view that allows users to create new requests"""
    user = request.user

    if user.user_type == 'ADM':
        return redirect('/admin')

    if request.method == "POST":

        request_type = request.POST.get('requestType')

        if request_type == 'SC' and user.user_object.type == 'PR':
            schedule = request.POST.getlist('schedule')
            start_time = request.POST.get('start_time')

            # Create schedule model
            monday_start = tuesday_start = wednesday_start = None
            thursday_start = friday_start = saturday_start = sunday_start = None

            for day in schedule:
                if day == 'MO':
                    monday_start = start_time
                elif day == 'TU':
                    tuesday_start = start_time
                elif day == 'WE':
                    wednesday_start = start_time
                elif day == 'TH':
                    thursday_start = start_time
                elif day == 'FR':
                    friday_start = start_time
                elif day == 'SA':
                    saturday_start = start_time
                elif day == 'SU':
                    sunday_start = start_time

                schedule_model = Schedule.objects.get_or_create(monday_start=monday_start,
                                                                tuesday_start=tuesday_start,
                                                                wednesday_start=wednesday_start,
                                                                thursday_start=thursday_start,
                                                                friday_start=friday_start,
                                                                saturday_start=saturday_start,
                                                                sunday_start=sunday_start)[0]

            request_change = None
        else:
            schedule_model = None
            request_change = request.POST.get('request_change')

        request = Request.objects.get_or_create(user_id=user, schedule_id=schedule_model,
                                                request_change=request_change,
                                                current_request_review_id=None,
                                                request_type=request_type)[0]

        request_review = RequestReview.objects.get_or_create(request_id=request,
                                                            status='P')[0]

        request.current_request_review_id = request_review
        request_review.save()
        request.save()

        # create new notification
        notification = Notification.objects.get_or_create(notification_type='R', is_dismissed=False,
                                                        request=request)[0]
        notification.save()

        # sending emails for this request:
        email_vendor.email_admin_new_request(request)
        email_vendor.email_user_new_request(request)

        return redirect('/requests')
    else:
        # GET Request
        return render(request, 'applications/request_new.html')


@login_required(login_url='/login')
def edit_request(request, id):
    """Edit request with given id
    """

    user = request.user

    if user.user_type == 'ADM':
        return redirect('/admin')

    if request.method == 'POST':
        if request.method == "POST":

            req = Request.objects.get(id=id)
            request_change = None

            if req.request_type == 'SC':
                schedule = request.POST.getlist('schedule')
                start_time = request.POST.get('start_time')

                # Create schedule model
                monday_start = tuesday_start = wednesday_start = None
                thursday_start = friday_start = saturday_start = sunday_start = None

                seen = {'SU': 0, 'MO': 0, 'TU': 0, 'WE': 0, 'TH': 0, 'FR': 0, 'SA': 0}
                for day in schedule:
                    if day == 'MO':
                        req.schedule_id.monday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'TU':
                        req.schedule_id.tuesday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'WE':
                        req.schedule_id.wednesday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'TH':
                        req.schedule_id.thursday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'FR':
                        req.schedule_id.friday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'SA':
                        req.schedule_id.saturday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1
                    elif day == 'SU':
                        req.schedule_id.sunday_start = string_to_object_time_converter(start_time)
                        seen[day] += 1

                count = 0
                for item in seen.items():
                    if item[1] == 0:
                        if count == 0:
                            req.schedule_id.sunday_start = None
                        if count == 1:
                            req.schedule_id.monday_start = None
                        if count == 2:
                            req.schedule_id.tuesday_start = None
                        if count == 3:
                            req.schedule_id.wednesday_start = None
                        if count == 4:
                            req.schedule_id.thursday_start = None
                        if count == 5:
                            req.schedule_id.friday_start = None
                        if count == 6:
                            req.schedule_id.saturday_start = None
                    count += 1

                req.schedule_id.save()
            else:
                request_change = request.POST.get('request_change')
                request.request_change = request_change

            req.save()

            return redirect('/requests')

    else:
        needed_request = Request.objects.get(id=id)
        needed_schedule = needed_request.schedule_id
        return render(request, 'applications/request_edit.html', context={"schedule": needed_schedule,
                                                                        "id": id, "req": needed_request})


class SingleRequest(generic.DetailView):
    """Extends DetailView class by using Request as a model."""
    model = Request

class ListSchoolRequests(generic.ListView):
    """Implements ListView class by using Request as a model"""
    model = Request

    def get_queryset(self):
        """Return requests where user is currently logged in user."""
        return Request.objects.filter(user_id=self.request.user)


@login_required(login_url='/admin/login')
def show_notifications(request):
    """Implements view that displays list of available notifications to admins."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    new_notifications = Notification.objects.order_by('-created_at')
    return render(request, 'admin/notifications.html', context={'notifications': new_notifications})


@login_required(login_url='/admin/login')
def visit_notification(request, id):
    """Implements view that allows admins to view notification details."""
    if request.user.user_type == 'BSC':
        return redirect('/')

    notification = Notification.objects.get(id=id)
    notification.is_dismissed = True

    notification.save()

    if notification.notification_type == 'A':
        application_id = notification.application.id
        url_path = '/admin/application/{}/review'.format(application_id)
        return redirect(url_path)
    elif notification.notification_type == 'R':
        request_id = notification.request.id
        url_path = '/admin/request/{}/review'.format(request_id)
        return redirect(url_path)
    else:
        user_id = notification.basic_user.id
        url_path = '/admin/user/{}/'.format(user_id)
        return redirect(url_path)


@login_required(login_url='/admin/login')
def hover_notification(request, id):
    """Implements feature that allows admins to hover notification."""
    if request.method == "POST":
        if request.user.user_type == 'BSC':
            return redirect('/')

        notification = Notification.objects.get(id=id)
        notification.is_dismissed = True
        notification.save()
        return JsonResponse({'value': True})
    else:
        return JsonResponse({'value': False})


@login_required(login_url='/admin/login')
def dismiss_all_notifications(request):
    """Implements feature that allows admins to dismiss notification"""
    if request.user.user_type == 'BSC':
        return redirect('/')

    notifications = Notification.objects.order_by('-created_at')
    for notification in notifications.filter(is_dismissed=0):
        notification.is_dismissed = True
        notification.save()
    return render(request, 'admin/notifications.html', context={'notifications': notifications})
