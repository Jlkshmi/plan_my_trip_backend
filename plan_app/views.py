import json
from datetime import datetime

import app
from django.conf import settings
from django.contrib.auth import authenticate, login
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from plan_app.forms import Userregister, Managerregister
from plan_app.models import HotelReview, HomeStayReview, HomestayPayment, HotelPayment
from plan_app.serializer import BookingSerializer, HotelReviewSerializer, HomestayReviewSerializer,HomestayBookingSerializer




@csrf_exempt
def user_registration(request):
    result_data=None
    if request.method=='POST':
        form=Userregister(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.is_active=True
            form.is_user=True
            form.save()
            result_data=True
    try:
        if result_data:
            data={'result':True}
        else:
            print(list(form.errors))
            error_data=form.errors
            error_dict={}
            for i in list(form.errors):
                error_dict[i]=error_data[i][0]
                data={
                    'result':False,
                    'errors':error_dict
                }
    except:
        data={
            'result':False
        }
    return JsonResponse(data,safe=False)

@csrf_exempt
def manager_registration(request):
    result_data=None
    if request.method=='POST':
        form=Managerregister(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.is_active=True
            form.is_manager=True
            form.save()
            result_data=True
    try:
        if result_data:
            data={'result':True}
        else:
            print(list(form.errors))
            error_data=form.errors
            error_dict={}
            for i in list(form.errors):
                error_dict[i]=error_data[i][0]
                data={
                    'result':False,
                    'errors':error_dict
                }
    except:
        data={
            'result':False
        }
    return JsonResponse(data,safe=False)



@csrf_exempt
def user_login(request):
        print(request.POST)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password1')
        print(password)
        user = authenticate(request, username=username,password=password)
        print(user)
        if user is not None:
            if user.is_blocked:
                return Response({"message": "User is blocked"}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            if user.is_user:
                user_type = 'user'
            elif user.is_manager:
                user_type = 'manager'
            elif user.is_staff:
                user_type = 'admin'
            else:
                user_type = 'unknown'
            data = {
                'status': True,
                'result': {
                    'id': user.id,
                    'name': user.name,
                    'username':user.username,
                    'type': user_type,
                    'phone':user.phone,
                    'address':user.address,
                    'email':user.email,
                    'is_blocked': user.is_blocked
                }
            }
        else:
            data = {
                'status': False,
                'result': 'Invalid username or password'
            }
        return JsonResponse(data, safe=False)


class HotelReviewCreateView(APIView):
    def post(self, request):
        serializer = HotelReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelReview_Get(APIView):
    def get(self,request,id):
        hotels = HotelReview.objects.filter(hotel=id)
        serializer = HotelReviewSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomestayCreateView(APIView):
    def post(self,request):
        serializer = HomestayReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomestayReview_Get(APIView):
    def get(self,request,id):
        homestay = HomeStayReview.objects.filter(homestays=id)
        serializer = HomestayReviewSerializer(homestay,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def Homestay_create_booking(request):
    serializer = HomestayBookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





stripe.api_key = settings.STRIPE_SECRET_KEY
class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            amount = request.data.get('amount')
            payer_id = request.data.get('payer_id')


            payment = HomestayPayment.objects.create(
                payment_id='checkout_session.id',
                payer_id=payer_id,
                amount=amount,
                currency='INR',
                status='Pending'
            )
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1PoI19Rvo8X3vQNbHnZbYUrX',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('http://localhost:5173/'),
                cancel_url=request.build_absolute_uri('/canceled'),
            )


            payment.payment_id = checkout_session.id
            payment.save()

            return Response({'id': checkout_session.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


stripe.api_key = settings.STRIPE_SECRET_KEY

class HotelStripeCheckoutView(APIView):
    def post(self, request):
        try:
            amount = request.data.get('amount')
            payer_id = request.data.get('payer_id')
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1PoI19Rvo8X3vQNbHnZbYUrX',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('http://localhost:5173/'),
                cancel_url=request.build_absolute_uri('/canceled'),
            )
            payment = HotelPayment.objects.create(
                payment_id=checkout_session.id,
                payer_id=payer_id,
                amount=amount,
                currency='INR',
                status='Pending'
            )

            return Response({'id': checkout_session.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




