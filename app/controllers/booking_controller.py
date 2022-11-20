import datetime

import django.db.models

from ..models import Service, Booking, Saloon
from django.forms.models import model_to_dict
from django.db.models import TimeField

minutes_per_slot = 30
minutes_to_consider = ["00", "30"]


def get_bookings(saloon_id):
    output_json = {}
    service_list = []
    for service in Booking.objects.filter(saloon_id=saloon_id):
        service_list.append(model_to_dict(service))
    output_json["bookings"] = service_list
    return output_json


def book(saloon_id, service_id, booking_date, booking_time):
    return check_slot_availability_and_book(saloon_id, service_id, booking_date, booking_time)


def check_slot_availability_and_book(saloon_id, service_id, booking_date, booking_time):
    saloon = Saloon.objects.get(saloon_id=saloon_id)
    service = Service.objects.get(service_id=service_id)
    bookings = Booking.objects.filter(saloon_id=saloon_id, booking_date=booking_date)

    st_time = booking_time
    end_time = add_minutes_time(booking_time, service.time_taken)
    # print(st_time, end_time)
    filtered_bookings = bookings.filter(start_time__gte=st_time)
    filtered_bookings = filtered_bookings.filter(end_time__lte=end_time)

    if len(filtered_bookings) >= saloon.number_of_seats:
        return "Sorry the requested slot is not available"
    new_booking = Booking(
        saloon_id=saloon,
        service_id=service,
        booking_date=booking_date,
        start_time=booking_time,
        end_time=end_time
    )
    new_booking.save()
    return f"Your booking is successful with booking id : {new_booking.booking_id}"


def get_available_slots_for_booking(saloon_id, service_id, booking_date):
    saloon = Saloon.objects.get(saloon_id=saloon_id)
    service = Service.objects.get(service_id=service_id)
    bookings = Booking.objects.filter(saloon_id=saloon_id, booking_date=booking_date)
    # print(f"Total bookings on that date {len(bookings)}")
    """
    Calculate booking time with 
    1. bookings on that date
    2. time taken for the selected service
    3. No of seats available in the saloon
    """
    available_time_slots = []
    all_time_slots = populate_time_slots(saloon.open_time.hour, saloon.close_time.hour)
    if saloon.close_time.minute != 30:
        all_time_slots.pop(-1)

    for time_slot in all_time_slots:
        st_time = time_slot
        end_time = add_minutes_time(time_slot, service.time_taken)
        # print(st_time, end_time)
        filtered_bookings = bookings.filter(start_time__gte=st_time)
        filtered_bookings = filtered_bookings.filter(end_time__lte=end_time)
        # print(len(filtered_bookings), saloon.number_of_seats)
        if len(filtered_bookings) < saloon.number_of_seats:
            available_time_slots.append(time_slot)

    return {"slots": available_time_slots}


def populate_time_slots(start_hour, end_hour):
    time_slots = []
    for i in range(start_hour, end_hour + 1):
        for j in minutes_to_consider:
            time_slots.append(f"{i:02d}:{j}:00")
    return time_slots


def add_minutes_time(start_time, minutes):
    time = datetime.datetime.strptime(start_time, "%H:%M:%S")
    out = time + datetime.timedelta(minutes=minutes)
    return str(out.time())
