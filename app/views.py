import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Saloon, Booking, Service
from django.template import loader
from django.forms.models import model_to_dict
from .controllers import booking_controller


# Create your views here.
def home(request):
    print("Hello")
    template = loader.get_template("app/index.html")
    return HttpResponse(template.render())


def get_all_saloons(request):
    output_json = {}
    saloon_list = []
    for saloon in Saloon.objects.all():
        saloon_list.append(model_to_dict(saloon))
    output_json["saloons"] = saloon_list
    return JsonResponse(output_json)


def get_all_bookings(request):
    output_json = {}
    booking_list = []
    for booking in Booking.objects.all():
        booking_list.append(model_to_dict(booking))
    output_json["saloons"] = booking_list
    return JsonResponse(output_json)


def get_saloon_services(request, saloon_id):
    output_json = {}
    service_list = []
    for service in Service.objects.filter(saloon_id=saloon_id):
        service_list.append(model_to_dict(service))
    output_json["services"] = service_list
    return JsonResponse(output_json)


def get_bookings_by_time(request):
    output_json = {}
    booking_list = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    check_for_time = body["check_for_time"]
    bookings = Booking.objects.filter(start_time__lte=check_for_time)
    print(bookings)
    objects = bookings.filter(end_time__gte=check_for_time)
    print(objects)
    print(len(objects))
    for booking in objects:
        booking_list.append(model_to_dict(booking))
    output_json["bookings"] = booking_list
    return JsonResponse(output_json)


def add_mins(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    check_for_time = body["check_for_time"]
    output = {"new_time": booking_controller.add_minutes_time(check_for_time, 45)}
    return JsonResponse(output)


def get_saloons_availability_on_date(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    saloon_id = body["saloon_id"]
    service_id = body["service_id"]
    booking_date = body["booking_date"]
    slots = booking_controller.get_available_slots_for_booking(saloon_id, service_id, booking_date)
    return JsonResponse(slots)


def book_saloon_service(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    saloon_id = body["saloon_id"]
    service_id = body["service_id"]
    booking_date = body["booking_date"]
    booking_time = body["booking_time"]
    out = {"status": booking_controller.book(saloon_id, service_id, booking_date, booking_time)}
    return JsonResponse(out)
