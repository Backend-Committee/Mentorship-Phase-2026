
from rest_framework import serializers

from banks.models import Bank, BankAccount, BankAdmin, Card


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name']

class BankAccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BankAccount
        fields = ['id','balance', 'first_name', 'last_name']

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        # Automatically create a card
        import random
        from datetime import date, timedelta

        card = Card.objects.create(
            card_number="".join([str(random.randint(0, 9)) for _ in range(16)]),
            expiration_date=date.today() + timedelta(days=365*3),  # 3 years
            cvv="".join([str(random.randint(0, 9)) for _ in range(3)]),
            networkProvider=random.choice(["Visa", "MasterCard"]),
            card_holder_name=f"{first_name} {last_name}"
        )

        # Create the bank account
        account = BankAccount.objects.create(
            card=card,
            **validated_data  # contains user_id, balance, bank_id from perform_create
        )
        return account

class BankAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAdmin
        fields = ['id', 'bank', 'user']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_number', 'expiration_date', 'cvv', 'networkProvider', 'card_holder_name']
