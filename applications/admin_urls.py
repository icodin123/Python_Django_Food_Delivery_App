from django.conf.urls import url, include
from . import views

urlpatterns = [
    # urls for school requests - user side
    url(r"^$", views.admin_homepage, name="adminhome"),
    url(r"^login/$", views.admin_login, name="admin_login"),
    url(r"^settings/$", views.admin_settings, name="admin_settings"),
    url(r"^settings/", include("applications.settings_urls", namespace="admin_settings")),
    url(r"^applications/$", views.applications, name="applications"),
    url(r"^requests/$", views.requests, name="requests"),

    url(r"^programs/$", views.programs, name="programs"),
    url(r"^restaurants/$", views.restaurants, name="restaurants"),
    url(r"^resources/$", views.resources, name="resources"),

    # review urls for applications
    url(r"^application/(?P<id>[0-9]+)/review/$", views.application_review, name="review"),
    url(r"^application/(?P<id>[0-9]+)/accept/$", views.accept, name="accept"),
    url(r"^application/(?P<id>[0-9]+)/deny/$", views.deny, name="deny"),

    # review urls for requests
    url(r"^request/(?P<id>[0-9]+)/review/$", views.review_request, name="review_request"),
    url(r"^request/(?P<id>[0-9]+)/accept/$", views.accept_request, name="accept_request"),
    url(r"^request/(?P<id>[0-9]+)/deny/$", views.deny_request, name="deny_request"),
    
    url("^program/(?P<id>[0-9]+)/$", views.program_profile, name="program"),
    url("^program/(?P<id>[0-9]+)/add_note$", views.add_program_note, name="new_program_note"),
    url("^program/(?P<id>[0-9]+)/add_contact$", views.add_program_contact,
        name="new_program_contact"),

    url(r"^restaurant/(?P<id>[0-9]+)/$", views.restaurant_profile, name="restaurant"),
    url(r"^restaurant/(?P<id>[0-9]+)/add_note$", views.add_restaurant_note, name="new_restaurant_note"),
    url(r"^restaurant/(?P<id>[0-9]+)/add_contact$", views.add_restaurant_contact, name="new_restaurant_contact"),

    # view specific user profile
    url(r"^user/(?P<id>[0-9]+)/$", views.view_user_profile, name="user_profile"),
    url(r"^user/(?P<id>[0-9]+)/edit$", views.edit_user_profile, name="edit_user_profile"),

    url(r"^pairings/$", views.pairings, name="pairings"),
    url(r"^pairings/add$", views.pairings_add, name="new_pairing"),
    url(r"^pairings/delete$", views.pairings_delete, name="delete_pairing"),

    # url routing for notifications page
    url(r"^notifications/$", views.show_notifications, name="notifications"),
    url(r"^notifications/(?P<id>[0-9]+)/visit/$", views.visit_notification, name="visit_notifications"),
    url(r"^notifications/(?P<id>[0-9]+)/hover/$", views.hover_notification, name="hover_notifications"),
    url(r"^notifications/dismiss_all/$", views.dismiss_all_notifications, name="dismiss_notifications"),

    url(r"^mealhistory/$", views.meal_history, name="meal_history"),
    url(r"^mealhistory/update$", views.meal_history_update, name="meal_history_update"),

]
