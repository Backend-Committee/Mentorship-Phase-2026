from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from transactions.models import Transaction
from accounts.models import Account
from audit.models import AuditLog
import uuid

class PaymentViewSet(viewsets.ModelViewSet):
    # Mock Payment Gateway Integration
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_intent(self, request):
        """
        Mock Stripe Payment Intent Creation
        """
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'usd')
        
        if not amount:
             return Response({'error': 'Amount required'}, status=status.HTTP_400_BAD_REQUEST)

        # In real world: intent = stripe.PaymentIntent.create(...)
        # We mock it:
        client_secret = f"pi_{uuid.uuid4()}_secret_{uuid.uuid4()}"
        payment_intent_id = f"pi_{uuid.uuid4()}"
        
        # Store initial payment record
        try:
             # Associate with user's primary account by default or passed param
             acc = request.user.accounts.first() 
             if not acc:
                  return Response({'error': 'User has no account'}, status=status.HTTP_400_BAD_REQUEST)
             
             Payment.objects.create(
                 user=request.user,
                 amount=amount,
                 gateway='Stripe',
                 payment_reference=payment_intent_id,
                 status=Payment.PaymentStatus.PENDING
             )
        except Exception as e:
             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'client_secret': client_secret,
            'id': payment_intent_id
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def webhook(self, request):
        """
        Mock Stripe Webhook Handler
        """
        # Verify signature would go here
        event = request.data
        
        if event.get('type') == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            payment_intent_id = payment_intent['id']
            amount = payment_intent['amount'] # Stripe in cents
            
            try:
                payment = Payment.objects.get(payment_reference=payment_intent_id)
                if payment.status == Payment.PaymentStatus.COMPLETED:
                     return Response({'status': 'exists'}, status=200)

                payment.status = Payment.PaymentStatus.COMPLETED
                payment.save()
                
                # Create DEPOSIT Transaction
                user_account = payment.user.accounts.first()
                if user_account:
                    Transaction.objects.create(
                        account=user_account,
                        transaction_type=Transaction.TransactionType.DEPOSIT,
                        amount=payment.amount,
                        status=Transaction.TransactionStatus.COMPLETED,
                        description=f"Stripe Payment {payment_intent_id}"
                    )
                    user_account.balance += payment.amount
                    user_account.save()
                    
                    AuditLog.objects.create(
                        user=payment.user,
                        action="PAYMENT_SUCCESS",
                        details={'amount': str(payment.amount), 'payment_id': payment.id}
                    )
                    
                return Response({'status': 'success'}, status=200)
                
            except Payment.DoesNotExist:
                 return Response({'status': 'payment not found'}, status=404)
        
        return Response({'status': 'ignored'}, status=200)

