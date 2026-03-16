from rest_framework import serializers
from .models import  Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'appointment')

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Value must be greater than 0")
        return value

    def validate(self, data):
        account = data.get('account')
        type = data.get('type')
        value = data.get('value')
        transfer_to = data.get('transfer_to')

        if type == 'Withdraw' or type ==  'Transfer':
            if value > account.balance:
                raise serializers.ValidationError("Your balance is smaller than the transaction value")

        if type == 'Transfer':
            if not transfer_to:
                raise serializers.ValidationError("You must select a transfer account")
            if account == transfer_to:
                raise serializers.ValidationError("You cannot transfer to the same account")

        return data

