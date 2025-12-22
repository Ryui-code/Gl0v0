import secrets
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'status',
            'data_registered',
            'token'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'token': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['token'] = secrets.token_hex(16)
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise ValidationError('Incorrect credentials')
        return {'user': user}

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['token']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise ValidationError('Invalid token.')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'store_image', 'store_name', 'description', 'category', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6', 'item_7', 'item_8', 'item_9', 'item_10', 'owner', 'username', 'contact_phone_number', 'website', 'average_rating']
        read_only_fields = ['owner'] # писать все вручную когда используется def avg_rating(self):

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def get_username(self, obj):
        return obj.owner.username

class StoreRatingSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()

    class Meta:
        model = StoreRating
        fields = ['id', 'store', 'store_name', 'rate', 'description', 'created_date']

    def get_store_name(self, obj):
        return obj.store.store_name

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CourierRatingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = CourierRating
        fields = ['id', 'courier', 'username', 'rate', 'description', 'created_date']

    def get_username(self, obj):
        return obj.courier.username