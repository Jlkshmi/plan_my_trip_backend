from rest_framework import serializers

from plan_app.models import Login, HomeStayDestination, Homestays, HomestayImage, HotelDestination, \
     HotelImage, Hotels, Bookings, HotelReview, HomeStayReview, HomestayBooking, \
    HomestayPayment


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields=('username','password','is_user','name','email','phone','address','is_blocked','id')

class Manager_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields=('username','password','is_manager','email','company_name','company_address','phone','id')

class add_destination_serializer(serializers.ModelSerializer):
    class Meta:
        model=HomeStayDestination
        fields=('image','destination_name')
class Hotel_destination_serializer(serializers.ModelSerializer):
    class Meta:
        model = HotelDestination
        fields=['image','destination_name']



class HomestayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomestayImage
        fields = ['id', 'images']

class HomestaysSerializer(serializers.ModelSerializer):
    images = HomestayImageSerializer(many=True, read_only=True)

    class Meta:
        model = Homestays
        fields = ['id', 'name', 'facilities', 'cash', 'state', 'details', 'address','city','images']

class HomestaysCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )

    class Meta:
        model = Homestays
        fields = ['name', 'facilities', 'cash', 'state', 'details','address','city','images']

    def create(self, validated_data):
        images = validated_data.pop('images')
        homestay = Homestays.objects.create(**validated_data)
        for image in images:
            HomestayImage.objects.create(homestay=homestay, images=image)
        return homestay

class HomestayReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStayReview
        fields = ['homestays','rating','comment','user_name']


class HomestayDetailsSerializer(serializers.ModelSerializer):
    homestay = HomestaysSerializer()
    user = User_Serializer()
    class Meta:
        model = HomestayBooking
        fields = ['user','homestay','check_in_date','check_out_date','number_of_rooms','room_type','total_price']
class HomestayBookingSerializer(serializers.ModelSerializer):
    homestay = serializers.PrimaryKeyRelatedField(queryset=Homestays.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=Login.objects.all())
    class Meta:
        model = HomestayBooking
        fields = ['user','homestay','check_in_date','check_out_date','number_of_rooms','room_type','total_price']



class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'images']

class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True,read_only=True)
    class Meta:
        model = Hotels
        fields=['id','name','description','address','city',
                'state','details','phone_number','facilities',
                'price_per_night','created_at','updated_at',
                'average_rating','number_of_reviews','images']

class HotelCreateSerializers(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    class Meta:
        model = Hotels
        fields = ['name','description','address','city',
                'state','details','phone_number','facilities',
                'price_per_night','created_at','updated_at',
                'average_rating','number_of_reviews','images']
    def create(self, validated_data):
        images = validated_data.pop('images')
        hotel = Hotels.objects.create(**validated_data)
        for image in images:
            HotelImage.objects.create(hotels=hotel, images=image)
        return hotel

class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = ['hotel','rating', 'comment','user']


class BookingDetailSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    user = User_Serializer()
    class Meta:
        model = Bookings
        fields = ['user', 'hotel', 'check_in_date', 'check_out_date', 'number_of_rooms', 'room_type','total_price']
class BookingSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotels.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=Login.objects.all())
    class Meta:
        model = Bookings
        fields = ['user', 'hotel', 'check_in_date', 'check_out_date', 'number_of_rooms', 'room_type','total_price']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomestayPayment
        fields = ['payment_id', 'payer_id', 'amount', 'currency', 'status', 'created_at', 'updated_at']

