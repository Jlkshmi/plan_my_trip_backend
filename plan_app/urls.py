from django.urls import path
from plan_app import views, adminviews, managerviews
from plan_app.adminviews import delete_homestay, delete_hotel, BlockUserView
from plan_app.managerviews import get_hotels_by_destination, get_homestay_by_destination

from plan_app.views import create_booking, HotelReviewCreateView, HotelReview_Get, HomestayCreateView, \
    HomestayReview_Get, Homestay_create_booking, StripeCheckoutView, HotelStripeCheckoutView

urlpatterns = [
    path('login',views.user_login,name='login'),
    path("user_registration",views.user_registration,name='user_registration'),
    path("manager_registration",views.manager_registration,name='manager_registration'),
    path('hotel_reviews',HotelReviewCreateView.as_view(), name='hotel_review-create'),
    path('hotel_review_get/<int:id>/',HotelReview_Get.as_view(),name='hotel_review_get'),
    path('hotel_bookings', create_booking, name='create_booking'),
    path('homestay_reviews',HomestayCreateView.as_view(),name='homestay_reviews'),
    path('homestay_review_get/<int:id>',HomestayReview_Get.as_view(),name='homestay_review_get'),
    path('homestay_bookings', Homestay_create_booking, name='homestay_create_booking'),
    path('stripe_checkout', StripeCheckoutView.as_view(), name='stripe_checkout'),
    path('hotel_stripe_checkout',HotelStripeCheckoutView.as_view(),name='hotel_stripe_checkout'),
    path('hotels/<str:destination_name>/', get_hotels_by_destination, name='get_hotels_by_destination'),
    path('homestays/<str:destination_name>/',get_homestay_by_destination,name='get_homestay_by_destination'),


    # admin
    path('homestay_destination_add',adminviews.homestay_destination_add.as_view()),
    path('hotel_destination_add',adminviews.Hotel_destination_add.as_view()),
    path('user_count_view',adminviews.UserCountView.as_view()),
    path('manager_count_view',adminviews.ManagerCountView.as_view()),
    path('hotel_bookings_list_view',adminviews.BookingListCreateView.as_view()),
    path('homestay_booking_list_view',adminviews.Homestay_booking_Get.as_view()),
    path('user_list',adminviews.User_list.as_view()),
    path('manager_list',adminviews.Manager_list.as_view()),
    path('delete_homestay/<int:id>/',delete_homestay, name='delete_homestay'),
    path('delete_hotel/<int:id>/',delete_hotel,name='delete_hotel'),
    path('block_user/<int:id>/',adminviews.BlockUserView.as_view()),
    path('block_manager/<int:id>/',adminviews.BlockManagerView.as_view()),




    # manager
    path('add_homestays',managerviews.Homestays_Add.as_view()),
    path('get_homestays',managerviews.Homestays_Get.as_view()),
    path('get_homestays/<int:id>/',managerviews.Homestays_Get_Id.as_view()),
    path('add_hotels',managerviews.Hotel_Add.as_view()),
    path('get_hotels',managerviews.Hotel_Get.as_view()),
    path('get_hotels/<int:id>/',managerviews.Hotel_Get_Id.as_view()),
    path('HotelBookingListCreateView',managerviews.HotelBookingListCreateView.as_view()),
    path('HotelBookingsDelete/<int:id>/',managerviews.delete_hotel_Bookings,name='HotelBookingsDelete'),
    path('HomestayBookingListCreateView',managerviews.Homestay_booking_Get.as_view()),

]