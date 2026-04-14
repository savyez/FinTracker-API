from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, TransactionSerializer
from .models import Category, Transaction
from django.db.models import F, Sum
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related('category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionSummaryViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        summary = (
            transactions
            .values('category__name', transaction_type=F('type'))
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        return Response({
            'message': 'Successfully calculated summary',
            'data': {
                'user': request.user.username,
                'summary': summary
            }
        })


class TransactionTotalViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total income and expense',
            'data':{
                'user': request.user.username,
                'transaction_count': transactions.count(),
                'total': total
                }})


class TotalIncomeViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user, type='income')
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total income',
            'data': {
                'user': request.user.username,
                'total_income': total
            }
        })


class TotalExpenseViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user, type='expense')
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total expense',
            'data': {
                'user': request.user.username,
                'total_expense': total
            }
        })


class NetBalanceViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        net_balance = total_income - total_expense
        if net_balance >= 0:
            balance_status = 'Cheers! You are in surplus.'
        else:
            balance_status = 'Oops! You are in debt.'

        return Response({
            'message': 'Successfully calculated net balance',
            'data': {
                'user': request.user.username,
                'net_balance': net_balance,
                'balance_status': balance_status
            }
        })