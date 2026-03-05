from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Person, Staff, Customer, AccountType, Account
from django.db import transaction

# To be used with staff and customer serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

# To be used with staff and customer serializers
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["national_id", "full_name", "mobile_number", "email"]


class StaffSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    person = PersonSerializer()
        
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        person_data = validated_data.pop("person")
        user = User.objects.create_user(**user_data)
        person = Person.objects.create(user=user, **person_data)
        staff = Staff.objects.create(person=person)
        
        return staff

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        person_data = validated_data.pop("person", None)
        
        if user_data:
            user = instance.person.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        if person_data:
            person = instance.person
            for attr, value in person_data.items():
                setattr(person, attr, value)
            person.save()
        
        return instance

class CustomerSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    person = PersonSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        person_data = validated_data.pop("person")
        user = User.objects.create_user(**user_data)
        person = Person.objects.create(user=user, **person_data)
        customer = Customer.objects.create(person=person)
        
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        person_data = validated_data.pop("person", None)
        
        if user_data:
            user = instance.person.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        if person_data:
            person = instance.person
            for attr, value in person_data.items():
                setattr(person, attr, value)
            person.save()
        
        return instance


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ["id", "name", "interest_frequency", "interest_rate", "maximum_daily_withdrawal", "maximum_monthly_withdrawal"]

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "account_type", "customer", "balance", "created_at"]
        read_only_fields = ["created_at"]
        extra_kwargs = {"customer": {"allow_null": False}}
