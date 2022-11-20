from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('saloons', views.get_all_saloons),
    path('services/<int:saloon_id>', views.get_saloon_services),
    path('bookings/<int:saloon_id>', views.get_all_bookings),
    path('bookingbytime', views.get_bookings_by_time),
    path('addtime', views.add_mins),
    path('getslots', views.get_saloons_availability_on_date),
    path('book', views.book_saloon_service)
]
