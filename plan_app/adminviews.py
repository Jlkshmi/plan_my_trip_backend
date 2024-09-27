from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from plan_app.models import HomeStayDestination, HotelDestination, Login, Bookings, HomestayBooking, Homestays, Hotels
from plan_app.serializer import add_destination_serializer, Hotel_destination_serializer, BookingSerializer, \
    User_Serializer, HomestayBookingSerializer, BookingDetailSerializer, HomestayDetailsSerializer, Manager_Serializer


class homestay_destination_add(generics.ListCreateAPIView):
    queryset = HomeStayDestination.objects.all()
    serializer_class = add_destination_serializer

class Hotel_destination_add(generics.ListCreateAPIView):
    queryset = HotelDestination.objects.all()
    serializer_class = Hotel_destination_serializer

class UserCountView(APIView):
    def get(self,request):
        user_count1= Login.objects.filter(is_user=True).count()
        return Response({"user_count1":user_count1})

class ManagerCountView(APIView):
    def get(self,request):
        user_count2= Login.objects.filter(is_manager=True).count()
        return Response({"user_count2":user_count2})


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Bookings.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingSerializer
        return BookingDetailSerializer

class Homestay_booking_Get(generics.ListCreateAPIView):
    queryset = HomestayBooking.objects.all()
    serializer_class = HomestayBookingSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HomestayBookingSerializer
        return HomestayDetailsSerializer

class User_list(APIView):
    def get(self,request):
        data1=Login.objects.filter(is_user = True)
        serializer= User_Serializer(data1,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Manager_list(APIView):
    def get(self,request):
        data2 = Login.objects.filter(is_manager = True)
        serializer = Manager_Serializer(data2,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_homestay(request, id):
    try:
        homestay = Homestays.objects.get(id=id)
    except Homestays.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    homestay.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_hotel(request, id):
    try:
        hotel = Hotels.objects.get(id=id)
    except Hotels.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    hotel.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class BlockUserView(APIView):
    def patch(self, request, id):
        user = get_object_or_404(Login, id=id)
        user.is_blocked = not user.is_blocked
        user.save()
        status_message = "blocked" if user.is_blocked else "unblocked"
        return Response({"message": f"User {status_message} successfully"}, status=status.HTTP_200_OK)


class BlockManagerView(APIView):
    def patch(self, request, id):
        manager = get_object_or_404(Login, id=id)
        manager.is_blocked = not manager.is_blocked
        manager.save()
        status_message = "blocked" if manager.is_blocked else "unblocked"
        return Response({"message": f"User {status_message} successfully"}, status=status.HTTP_200_OK)


