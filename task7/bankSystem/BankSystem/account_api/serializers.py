from rest_framework import serializers
from account.models import BankAccount, Transaction
from django.db import transaction
from django.contrib.auth.models import User

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'user', 'account_number', 'balance']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        # use create_user so password is properly hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        # if password is being updated, hash it properly
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    # Explicitly declare so we can control queryset dynamically
    sender = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(), required=False, allow_null=True
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'sender', 'receiver']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        t_type = None
        if request and request.data:
            t_type = request.data.get('transaction_type')

        if t_type == 'deposit':
            # only amount + receiver needed
            self.fields.pop('sender', None)
            self.fields['receiver'].queryset = BankAccount.objects.all()

        elif t_type == 'withdraw':
            # user picks which of their own accounts to withdraw from
            self.fields.pop('receiver', None)
            if request and request.user and request.user.is_authenticated:
                self.fields['sender'].queryset = BankAccount.objects.filter(user=request.user)
            else:
                self.fields['sender'].queryset = BankAccount.objects.all()

        elif t_type == 'transfer':
            # sender = logged-in user's own accounts
            # receiver = all accounts (full queryset so PK validation never fails)
            # ownership is enforced in validate()
            if request and request.user and request.user.is_authenticated:
                self.fields['sender'].queryset = BankAccount.objects.filter(user=request.user)
            self.fields['receiver'].queryset = BankAccount.objects.all()

    def validate(self, data):
        request = self.context['request']
        t_type = data.get('transaction_type')

        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError("Amount must be positive")

        # For withdraw/transfer, validate sender belongs to logged-in user
        if t_type in ('withdraw', 'transfer'):
            sender = data.get('sender')
            if not sender:
                raise serializers.ValidationError("Please select an account to send from")
            if sender.user != request.user:
                raise serializers.ValidationError("You can only use your own account as sender")

        if t_type == 'deposit' and not data.get('receiver'):
            raise serializers.ValidationError("Receiver is required for deposit")
        if t_type == 'transfer' and not data.get('receiver'):
            raise serializers.ValidationError("Receiver is required for transfer")
        if t_type == 'transfer' and data.get('receiver') and data.get('sender'):
            if data['receiver'] == data['sender']:
                raise serializers.ValidationError("Sender and receiver cannot be the same account")

        return data

    def create(self, validated_data):
        with transaction.atomic():
            transaction_type = validated_data['transaction_type']
            amount = validated_data['amount']

            if transaction_type == 'deposit':
                receiver = validated_data['receiver']
                receiver.balance += amount
                receiver.save()

            elif transaction_type == 'withdraw':
                sender = validated_data['sender']
                if sender.balance < amount:
                    raise serializers.ValidationError("Insufficient balance")
                sender.balance -= amount
                sender.save()

            elif transaction_type == 'transfer':
                sender = validated_data['sender']
                receiver = validated_data['receiver']
                if sender.balance < amount:
                    raise serializers.ValidationError("Insufficient balance")
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()

            return super().create(validated_data)
