# transactions/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date
from .models import Category, Transaction

User = get_user_model()


class TransactionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='StrongPass123!'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='StrongPass123!'
        )
        self.category_income = Category.objects.create(
            name='Salary',
            type='income',
            color='#00FF00',
            user=self.user
        )
        self.category_expense = Category.objects.create(
            name='Food',
            type='expense',
            color='#FF0000',
            user=self.user
        )
        self.transactions_url = reverse('transaction-list')
        self.summary_url = reverse('transaction-summary')

    def _auth(self, user=None):
        target = user or self.user
        self.client.force_authenticate(user=target)

    def _make_transaction(self, amount, type, category, d=None):
        return Transaction.objects.create(
            user=self.user,
            amount=Decimal(amount),
            type=type,
            category=category,
            date=d or date.today()
        )


class TransactionAuthTests(TransactionTests):

    def test_unauthenticated_cannot_post(self):
        payload = {
            'amount': '1000.00',
            'type': 'income',
            'category': self.category_income.id,
            'date': str(date.today()),
        }
        response = self.client.post(self.transactions_url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_post(self):
        self._auth()
        payload = {
            'amount': '1000.00',
            'type': 'income',
            'category': self.category_income.id,
            'date': str(date.today()),
        }
        response = self.client.post(self.transactions_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 1)

    def test_user_cannot_use_another_users_category(self):
        other_category = Category.objects.create(
            name='Other Salary',
            type='income',
            color='#0000FF',
            user=self.other_user
        )
        self._auth()
        payload = {
            'amount': '500.00',
            'type': 'income',
            'category': other_category.id,
            'date': str(date.today()),
        }
        response = self.client.post(self.transactions_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_see_other_users_transactions(self):
        self._make_transaction('1000.00', 'income', self.category_income)
        self._auth(self.other_user)

        response = self.client.get(self.transactions_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_transaction_type_must_match_category_type(self):
        self._auth()
        payload = {
            'amount': '500.00',
            'type': 'expense',            # expense type
            'category': self.category_income.id,  # but income category
            'date': str(date.today()),
        }
        response = self.client.post(self.transactions_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SummaryTests(TransactionTests):

    def setUp(self):
        super().setUp()
        self._auth()
        self._make_transaction('5000.00', 'income',  self.category_income, date(2024, 1, 15))
        self._make_transaction('3000.00', 'income',  self.category_income, date(2024, 1, 20))
        self._make_transaction('1200.00', 'expense', self.category_expense, date(2024, 1, 10))
        self._make_transaction('800.00',  'expense', self.category_expense, date(2024, 1, 25))
        self._make_transaction('9999.00', 'income',  self.category_income, date(2024, 2, 1))

    def test_summary_correct_totals(self):
        response = self.client.get(self.summary_url, {'month': '2024-01'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_income']),  Decimal('8000.00'))
        self.assertEqual(Decimal(response.data['total_expenses']), Decimal('2000.00'))
        self.assertEqual(Decimal(response.data['net_balance']),   Decimal('6000.00'))

    def test_summary_excludes_other_months(self):
        response = self.client.get(self.summary_url, {'month': '2024-01'})

        self.assertEqual(Decimal(response.data['total_income']), Decimal('8000.00'))

    def test_summary_empty_month(self):
        response = self.client.get(self.summary_url, {'month': '2023-06'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_income']),   Decimal('0.00'))
        self.assertEqual(Decimal(response.data['total_expenses']), Decimal('0.00'))
        self.assertEqual(Decimal(response.data['net_balance']),    Decimal('0.00'))

    def test_summary_requires_month_param(self):
        response = self.client.get(self.summary_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)