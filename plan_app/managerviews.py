from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from plan_app.models import Homestays, Hotels, Bookings, HomestayBooking
from plan_app.serializer import HomestaysCreateSerializer, HomestaysSerializer, \
    HotelCreateSerializers, HotelSerializer, BookingSerializer, BookingDetailSerializer, HomestayBookingSerializer, \
    HomestayDetailsSerializer


class Homestays_Add(APIView):
    def post(self, request):
        serializer = HomestaysCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Homestay and images uploaded successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Homestays_Get(APIView):
    def get(self, request):
        homestays = Homestays.objects.all()
        serializer = HomestaysSerializer(homestays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Homestays_Get_Id(APIView):
    def get(self, request, id=None):
        if id:
            homestay = get_object_or_404(Homestays, id=id)
            serializer = HomestaysSerializer(homestay)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            homestays = Homestays.objects.all()
            serializer = HomestaysSerializer(homestays, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class Hotel_Add(APIView):
    def post(self, request):
        serializer = HotelCreateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Hotel and images uploaded successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Hotel_Get(APIView):
    def get(self, request):
        hotel = Hotels.objects.all()
        serializer = HotelSerializer(hotel, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Hotel_Get_Id(APIView):
    def get(self, request, id=None):
        if id:
            hotel = get_object_or_404(Hotels, id=id)
            serializer = HotelSerializer(hotel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            hotel = Hotels.objects.all()
            serializer = HotelSerializer(hotel, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class HotelBookingListCreateView(generics.ListCreateAPIView):
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

@api_view(['DELETE'])
def delete_hotel_Bookings(request, id):
    try:
        hotel = Bookings.objects.get(id=id)
    except Bookings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    hotel.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_hotels_by_destination(request, destination_name):
    hotels = Hotels.objects.filter(state__iexact=destination_name)
    serialized_hotels = HotelSerializer(hotels, many=True)
    return Response(serialized_hotels.data)

@api_view(['GET'])
def get_homestay_by_destination(request, destination_name):
    homestays = Homestays.objects.filter(state__iexact=destination_name)
    serialized_hotels = HomestaysSerializer(homestays, many=True)
    return Response(serialized_hotels.data)