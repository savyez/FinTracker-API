from django.urls import path
from .views import (
        CategoryViewSet, TotalExpenseViewSet, TotalIncomeViewSet, TransactionSummaryViewSet, 
        TransactionTotalViewSet, TransactionViewSet, NetBalanceViewSet, TransactionsInsightView 
        )

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<uuid:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('transactions/', TransactionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transaction-list'),
    path('transactions/insights/', TransactionsInsightView.as_view({'get': 'list'}), name='transaction-insights'),
    path('transactions/<uuid:pk>/', TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='transaction-detail'),
    path('transactions/summary/', TransactionSummaryViewSet.as_view({'get': 'list'}), name='transaction-summary'),
    path('transactions/summary/total/', TransactionTotalViewSet.as_view({'get': 'list'}), name='transaction-total'),
    path('transactions/summary/total/income/', TotalIncomeViewSet.as_view({'get': 'list'}), name='total-income'),
    path('transactions/summary/total/expense/', TotalExpenseViewSet.as_view({'get': 'list'}), name='total-expense'),
    path('transactions/summary/net-balance/', NetBalanceViewSet.as_view({'get': 'list'}), name='net-balance'),
]