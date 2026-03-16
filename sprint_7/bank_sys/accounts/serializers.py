from rest_framework import serializers
from .models import User, Account

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'phone_num', 'DOB')
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__' # ['id', 'user', 'balance']

        def validate_balance(self, balance):
            if balance < 0:
                raise serializers.ValidationError("Balance cannot be negative")
            return balance



